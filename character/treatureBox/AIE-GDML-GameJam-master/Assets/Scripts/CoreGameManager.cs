using System.Collections;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using UnityEngine;

public class CoreGameManager : MonoBehaviour {

    public AudioClip backgroundMusic;

	// Use this for initialization
	void Start ()
    {
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    public void LoadLevel(string a_level)
    {
        SceneManager.LoadScene(a_level);
        Physics.gravity = new Vector3(0, -70f, 0);
    }

    public void QuitGame()
    {
        Application.Quit();
    }



}
