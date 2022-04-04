using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Fire : MonoBehaviour {

    public Light m_fireLight;
    public AnimationCurve animCurve;
    float offset;
    float time;
    public void Start()
    {
        m_fireLight = this.GetComponent<Light>();
        offset = Random.Range(0, 1000f);
    }

    public void Update()
    {
        time += Time.deltaTime * Random.value;
        m_fireLight.intensity = animCurve.Evaluate(Mathf.PingPong(time + offset, 1));
    }
}
