using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ParticleAutoDestroy : MonoBehaviour {

    public ParticleSystem part;

	void Start ()
    {
        {
            Destroy(gameObject, part.main.duration);
        }
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
