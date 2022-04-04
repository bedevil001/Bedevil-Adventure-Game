using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SkipLevel : MonoBehaviour {

    public LevelManager m_levelManager;
    public PlayerMovement m_player;
	// Use this for initialization
	void Start () {
        m_levelManager = GameObject.FindWithTag("LevelManager").GetComponent<LevelManager>();
        m_player = GameObject.FindWithTag("Player").GetComponent<PlayerMovement>();
	}
	
	// Update is called once per frame
	void Update () {
        for(int i = 0; i < Mathf.Min(9, m_levelManager.m_levels.Count); i++) {
            if (Input.GetKeyDown(KeyCode.Alpha1+i)) {
                m_levelManager.m_currentLevel = m_levelManager.m_levels[i];
                m_levelManager.SetupLevel();
                m_player.transform.position = m_levelManager.m_currentLevel.m_respawnPoint.transform.position;
                m_player.ResetVariables();
            }
        }
    }
}
