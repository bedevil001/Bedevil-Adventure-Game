using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class KillBoxScript : MonoBehaviour {

    public AudioClip deathSound;
    public LevelManager m_levelManager;
    public ParticleSystem playerDeathParticle;
    Transform playerPosition;

    private void Start()
    {
        m_levelManager = GameObject.FindWithTag("LevelManager").GetComponent<LevelManager>();
        playerDeathParticle = Resources.Load<ParticleSystem>("Death");
        deathSound = Resources.Load<AudioClip>("Player Death Sound");
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            if (playerDeathParticle != null)
            {
                playerPosition = GameObject.Find("Player").transform;
                Instantiate(playerDeathParticle, playerPosition.transform.position, playerPosition.transform.rotation);
            }
            m_levelManager.RestartLevel();
            SoundManager.PlaySFX(deathSound);
        }
    }
}
