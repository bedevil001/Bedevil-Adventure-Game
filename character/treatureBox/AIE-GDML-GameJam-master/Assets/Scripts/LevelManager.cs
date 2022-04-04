using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class LevelManager : MonoBehaviour {

    [Header("Global Level Properties")]
    public float m_cameraPanTime;

    public Level m_currentLevel;
    public Level m_previousLevel;
    
    public List<Level> m_levels;

    private PlayerMovement m_player;
    [HideInInspector]
    public UIManager m_uiManager;
    private Vector3 m_defaultGravity;
    public Camera m_camera;
    private float m_currentTime;



    // Use this for initialization
    void Start () {
		foreach(GameObject obj in GameObject.FindGameObjectsWithTag("Level"))
        {
            m_levels.Add(obj.GetComponent<Level>());
        }
        m_levels.Sort(delegate (Level l1, Level l2) { return l1.m_levelNumber.CompareTo(l2.m_levelNumber); });

        m_defaultGravity = Physics.gravity;
        m_player = GameObject.FindWithTag("Player").GetComponent<PlayerMovement>();
        m_uiManager = GameObject.FindWithTag("UIManager").GetComponent<UIManager>();
        m_camera = GameObject.FindWithTag("MainCamera").GetComponent<Camera>();
        m_currentLevel = m_levels[0];
        SetupLevel();

    }

    public void SetupLevel()
    {
        m_uiManager.SetupKeys(m_currentLevel.m_keysInLevel);
        m_uiManager.SetupMoves(m_currentLevel.m_movesAvailable, m_currentLevel.m_movesAvailable);
        StartCoroutine(PanCamera(3));
        ResetGravity();

    }

    public void CompleteLevel()
    {
        if (m_currentLevel.m_movesDone == m_currentLevel.m_platinumStarMoves)
        {
            Debug.Log("Platinum");
            m_currentLevel.m_starAwarded = Level.StarAwarded.Platinum;
            m_uiManager.DisplayStar(m_currentLevel.m_starAwarded, m_currentLevel);
        }
        else if (m_currentLevel.m_movesDone <= m_currentLevel.m_goldStarMoves)
        {
            Debug.Log("Gold");
            m_currentLevel.m_starAwarded = Level.StarAwarded.Gold;
            m_uiManager.DisplayStar(m_currentLevel.m_starAwarded, m_currentLevel);
        }
        else if (m_currentLevel.m_movesDone <= m_currentLevel.m_silverStarMoves)
        {
            Debug.Log("Silver");
            m_currentLevel.m_starAwarded = Level.StarAwarded.Silver;
            m_uiManager.DisplayStar(m_currentLevel.m_starAwarded, m_currentLevel);
        }
        else if (m_currentLevel.m_movesDone <= m_currentLevel.m_bronzeStarMoves)
        {
            Debug.Log("Bronze");
            m_currentLevel.m_starAwarded = Level.StarAwarded.Bronze;
            m_uiManager.DisplayStar(m_currentLevel.m_starAwarded, m_currentLevel);
        }
        m_previousLevel = m_currentLevel;
        for(int i = 0; i < m_levels.Count; i++)
        {
            if(m_currentLevel == m_levels[i])
            {
                if (m_currentLevel != m_levels.Last<Level>())
                {
                    m_currentLevel = m_levels[i + 1];
                }
                break;
            }
           
        }
        m_previousLevel.CloseDoor();

        ResetGravity();
    }

    public void RestartLevel() {
        if (m_currentLevel.m_keysCollected == m_currentLevel.m_keysInLevel) {
            m_currentLevel.CloseDoor();
        }
        m_player.transform.position = m_currentLevel.m_respawnPoint.transform.position;
        Physics.gravity = m_defaultGravity;
        m_uiManager.SetupKeys(m_currentLevel.m_keysInLevel);
        m_uiManager.SetupMoves(m_currentLevel.m_movesAvailable, m_currentLevel.m_movesAvailable);
        m_player.GetComponent<Rigidbody>().velocity = Vector3.zero;
        m_currentLevel.m_movesDone = 0;
        m_currentLevel.m_keysCollected = 0;

        m_currentLevel.ResetKeys();

        ResetGravity();
    }

    public void AddKey()
    {
        m_uiManager.AddKey();
        m_currentLevel.m_keysCollected++;
        if (m_currentLevel.m_keysCollected == m_currentLevel.m_keysInLevel)
        {
           m_currentLevel.OpenDoor();
        }
    }

    private void ResetGravity() {
        setGravityDirection(m_currentLevel.m_startingDirection);
        m_player.ResetVariables();
    }

    public void setGravityDirection(PlayerMovement.Direction a_direction) {
        float gravityValue = Mathf.Max(Mathf.Abs(Physics.gravity.x), Mathf.Max(Mathf.Abs(Physics.gravity.y), Mathf.Abs(Physics.gravity.z)));
        Vector3 gravity = Vector3.zero;
        switch (a_direction) {
            case PlayerMovement.Direction.KDown:
                gravity.y = -gravityValue;
                break;
            case PlayerMovement.Direction.KUp:
                gravity.y = gravityValue;
                break;
            case PlayerMovement.Direction.KLeft:
                gravity.x = -gravityValue;
                break;
            case PlayerMovement.Direction.KRight:
                gravity.x = gravityValue;
                break;
        }
        Physics.gravity = gravity;
    }


    IEnumerator PanCamera(float time)
    {
        m_currentTime = 0;
        while (m_currentTime < time)
        {
            m_currentTime += Time.deltaTime;
            if (m_currentLevel.m_levelCamPos != null)
                m_camera.transform.position = Vector3.Lerp(m_camera.transform.position, m_currentLevel.m_levelCamPos.position, m_currentTime / time);
            yield return null;
        }
    }
}
