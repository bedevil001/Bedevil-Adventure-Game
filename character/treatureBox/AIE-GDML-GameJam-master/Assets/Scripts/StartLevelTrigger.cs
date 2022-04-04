using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class StartLevelTrigger : MonoBehaviour
{
    public LevelManager m_levelManager;

   
    public bool m_active;
    
    public bool changeBackgroundMusic;
    public AudioClip newBackGroundMusic;
    
   
    //public Image m_levelStar;
    

    //public References m_references;

    private void Start()
    {
        m_levelManager = GameObject.FindWithTag("LevelManager").GetComponent<LevelManager>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(m_active)
        {
            if (other.CompareTag("Player"))
            {
                m_levelManager.CompleteLevel();
                m_levelManager.SetupLevel();
                m_active = false;
            }
            if (changeBackgroundMusic)
            {
                SoundManager.StopBGM(false, 0);
                SoundManager.PlayBGM(newBackGroundMusic, true, 5.0f);
            }

        }

    }
}
