using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandTrackerr : MonoBehaviour
{
    // Start is called before the first frame update

    public UDPReceive udpReceive;
    public GameObject[] handPoints;
    string data;

    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        data = udpReceive.data;
        data = data.Remove(0,1);
        data = data.Remove(data.Length-1,1);
        print(data);
    }
}
