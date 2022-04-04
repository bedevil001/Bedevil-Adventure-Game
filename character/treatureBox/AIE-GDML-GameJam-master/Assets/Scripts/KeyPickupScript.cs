using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class KeyPickupScript : MonoBehaviour
{
    Collider playerCollider;
    AudioClip keyPickup;
    public LevelManager m_levelManager;
    
    private void Start()
    {
        m_levelManager = GameObject.FindWithTag("LevelManager").GetComponent<LevelManager>();
        keyPickup = Resources.Load<AudioClip>("Key Pickup Sound");
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            SoundManager.PlaySFX(keyPickup);
            m_levelManager.AddKey();
            this.gameObject.SetActive(false);
        }
        
    }
}
