using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
//using Newtonsoft.Json;

public class ClientSocket : MonoBehaviour
{
	#region private members 	
	private TcpClient socketConnection;
	private Thread clientReceiveThread;

	public GameObject Player;

	public GameObject selff;

	public Dictionary<string,int> Agent_input = new Dictionary<string, int>();

    public Dictionary<string, int> Agent_input_public = new Dictionary<string, int>();

    public Dictionary<string, int> Agent_Output = new Dictionary<string, int>();

	public Dictionary<string, int> Agent_input_old;

    public bool IsSwitch = false;


    // testign with using arrays instead of dictionaries

    public List<int> TestSampleData;
    #endregion
    // Use this for initialization 	

    

    private void Awake()
    {
		Agent_input.Add("forward", 0);
		Agent_input.Add("backward", 0);
		Agent_input.Add("left", 0);
		Agent_input.Add("right", 0);
		Agent_input_old = Agent_input;
        Agent_input_public = Agent_input;

        // add a placeholder
        TestSampleData.Add(0);
        TestSampleData.Add(1);
        TestSampleData.Add(2);
        TestSampleData.Add(3);
        TestSampleData.Add(4);
    }
    void Start()
	{
		ConnectToTcpServer();
		SendMessage();
	}

	// Update is called once per frame
	void Update()
	{
		//print("Agent is " + Agent_input);
        // here we detect if the data has been returned by comparing 2 variables to check for a change, if changed then we make the agent act on this new input
        //if (Agent_input != Agent_input_old)
        //{
		//	// Here the data has changed
		//	Agent_input_old = Agent_input;
        //    Agent_input_public = Agent_input;
        //
        //    
        //    //print("AGENT HAS CHANGED");
        //    // Do something with the agent
        //    SendMessage();
		//}

        //if (IsSwitch)
        //{
        //    IsSwitch = false;
        //    SendMessage();
        //}
        


    }

	/// <summary> 	
	/// Setup socket connection. 	
	/// </summary> 	

	private void ConnectToTcpServer()
	{
		try
		{
			clientReceiveThread = new Thread(new ThreadStart(ListenForData));
			clientReceiveThread.IsBackground = true;
			clientReceiveThread.Start();
		}
		catch (Exception e)
		{
			Debug.Log("On client connect exception " + e);
		}
	}

	/// <summary> 	
	/// Runs in background clientReceiveThread; Listens for incomming data. 	
	/// </summary>     
	private void ListenForData()
	{
		try
		{
			socketConnection = new TcpClient("localhost", 8052);
			Byte[] bytes = new Byte[1024];
			while (true)
			{
				print("listening");
				// Get a stream object for reading 				
				using (NetworkStream stream = socketConnection.GetStream())
				{
					int length;
					// Read incomming stream into byte arrary. 					
					while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
					{
						var incommingData = new byte[length];
						Array.Copy(bytes, 0, incommingData, 0, length);
						// Convert byte array to string message. 						
						string serverMessage = Encoding.ASCII.GetString(incommingData);
						
						serverMessage = serverMessage.Replace("'", "");

                        //print(serverMessage);

                        //print("OMG HERE IS THE DATA " + serverMessage);

                        //serverMessage = @"{""forward"": ""0"", ""backward"": ""0"", ""left"": 0, ""right"": 0}";


                        // this is required to check for updates
                        //Agent_input = JsonUtility.FromJson<Dictionary<string, int>>(serverMessage);
                        
                        if (!IsSwitch)
                        {
                            IsSwitch = true;
                        }

                        serverMessage = serverMessage.Replace("[", "");
                        serverMessage = serverMessage.Replace("]", "");
                        // here we convert the string list to a class list by using an aids and stupid round about way where we split the list up and we add each value to a list class
                        string[] splitString = serverMessage.Split(char.Parse(","));

                        //print(splitString[0]);

                        // attempt to get persistent data using a list and not a dictionary 
                        //var dank_placeholder = JsonUtility.FromJson<Dictionary<string, int>>(serverMessage);
                        TestSampleData[0] = int.Parse(splitString[0]);
                        TestSampleData[1] = int.Parse(splitString[1]);
                        TestSampleData[2] = int.Parse(splitString[2]);
                        TestSampleData[3] = int.Parse(splitString[3]);
                        TestSampleData[4] = int.Parse(splitString[4]);

                        // here we then move the player based on the results
                        //Player.GetComponent<AgentSensory>().move();


                        //Debug.Log("server message received as: " + Agent_input);
                        // attempt to update object in unity with data
                        //Agent_input = serverMessage;
                    }
				}
			}
		}
		catch (SocketException socketException)
		{
			Debug.Log("Socket exception: " + socketException);
		}
	}
	/// <summary> 	
	/// Send message to server using socket connection. 	
	/// </summary> 	
	public void SendMessage()
	{
		
		if (socketConnection == null)
		{
			
			return;
		}
		try
		{
			
			// Get a stream object for writing. 			
			NetworkStream stream = socketConnection.GetStream();
			
			if (stream.CanWrite)
			{
				//string clientMessage = "This is a message from one of your clients.";
				// Set the message as the dict data from the agent
				string clientMessage = DictionaryToString(Player.GetComponent<AgentSensory>().InputData);

				// Convert string message to byte array.                 
				byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(clientMessage);
				// Write byte array to socketConnection stream.      
				
				stream.Write(clientMessageAsByteArray, 0, clientMessageAsByteArray.Length);
				//Debug.Log("Client sent his message - should be received by server");
			}
		}
		catch (SocketException socketException)
		{
			Debug.Log("Socket exception: " + socketException);
		}
	}

	public string DictionaryToString(Dictionary<string, int> dictionary)
	{
		string dictionaryString = "{";
		foreach (KeyValuePair<string, int> keyValues in dictionary)
		{
			dictionaryString += keyValues.Key + " : " + keyValues.Value + ", ";
		}
		return dictionaryString.TrimEnd(',', ' ') + "}";
	}
}