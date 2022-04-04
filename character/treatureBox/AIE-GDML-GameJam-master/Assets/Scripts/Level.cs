using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class Level : MonoBehaviour {

    [Header("Level Properties")]
    public int m_keysInLevel;
    public int m_movesAvailable;

    [Header("Current Gameplay")]
    public int m_keysCollected;
    public int m_movesDone;
   
   
   
    [Header("Bools")]
    public bool m_levelFailed;
    private bool m_levelComplete;

    public PlayerMovement.Direction m_startingDirection = PlayerMovement.Direction.KDown;

    public Transform m_respawnPoint;
    [HideInInspector]
    public Transform m_levelCamPos;
    private Door m_door;
    private LevelManager m_levelManager;

    public AudioClip m_doorOpenSFX;

    public int m_platinumStarMoves;
    public int m_goldStarMoves;
    public int m_silverStarMoves;
    public int m_bronzeStarMoves;

    public int m_levelNumber;
    public Image m_levelStar;

    public enum StarAwarded
    {
        Bronze,
        Silver,
        Gold,
        Platinum
    }
    public StarAwarded m_starAwarded;

    [System.Serializable]
    public struct GravityDirection {
        [HideInInspector]
        public string m_name;
        public bool m_allowDirection;
    }

    public GravityDirection[] m_gravityDirection = new GravityDirection[4];

    private KeyPickupScript[] m_ListOfKeys;

    private void Awake() {
        m_levelNumber = int.Parse(transform.name.Remove(0, "Level".Length)) - 1;
    }

    // Use this for initialization
    void Start() {
        m_doorOpenSFX = Resources.Load<AudioClip>("Door Unlock Sound");
        m_levelManager = GameObject.FindWithTag("LevelManager").GetComponent<LevelManager>();
        m_door = GetComponentInChildren<Door>();
        m_ListOfKeys = GetComponentsInChildren<KeyPickupScript>();
        m_levelStar = GameObject.FindWithTag("ScoreHolder").transform.GetChild(m_levelNumber).GetComponent<Image>();

    }

    public void OpenDoor() {
        SoundManager.PlaySFX(m_doorOpenSFX);
        m_door.m_animtor.SetTrigger("Open");
    }

    public void CloseDoor() {
        m_door.m_animtor.SetTrigger("Close");
    }

    public void ResetKeys() {
        foreach (KeyPickupScript key in m_ListOfKeys) {
            key.gameObject.SetActive(true);
        }
    }

    private void OnValidate() {
        for(int i = 0; i < m_gravityDirection.Length; i++) {
            m_gravityDirection[i].m_name = ((PlayerMovement.Direction)i).ToString().Remove(0,1);
        }
    }
}
