using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BGM : MonoBehaviour
{
    public AudioClip m_BGM;

	// Use this for initialization
	void Start ()
    {
        SoundManager.PlayBGM(m_BGM, false, 2.5f);
    }
	
}
