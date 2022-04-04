using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class References : MonoBehaviour {

    public List<Sprite> m_starSprites;
    public List<GameObject> m_stars;
    public Animator m_starAnim;


    // Use this for initialization
    void Start () {
        m_starAnim = GameObject.Find("StarHolder").GetComponent<Animator>();
        m_stars.Add(GameObject.Find("BronzeStar"));
        m_stars.Add(GameObject.Find("SilverStar"));
        m_stars.Add(GameObject.Find("GoldStar"));
        m_stars.Add(GameObject.Find("PlatStar"));
        m_starSprites[0] = Resources.Load<Sprite>("Sprites/BronzeStar");
        m_starSprites[1] = Resources.Load<Sprite>("Sprites/SilverStar");
        m_starSprites[2] = Resources.Load<Sprite>("Sprites/GoldStar");
        m_starSprites[3] = Resources.Load<Sprite>("Sprites/PlatStar");
    }
	
	// Update is called once per frame
	void Update () {
		
	}
}
