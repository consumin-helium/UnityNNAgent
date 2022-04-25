using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AgentSensory : MonoBehaviour
{

    public GameObject Goal;

    public GameObject SELF;

    public bool actualREset = false;

    public List<GameObject> Ground_Front;
    public List<int> PossibleDirections;

    public List<int> DirectionOfGoal;

    public GameObject evntmanager;

    // here we have a json dict that has all the data we need for the server

    public Dictionary<string, int> InputData = new Dictionary<string, int>();

    public List<Vector3> rayCastingPositions;
    // Start is called before the first frame update


    // define a float to show the closest the agent has been to the goal in this life, and if it gets closer then update this and reward it
    public float ClosestToGoal = 30f;

    
    void Start()
    {
        ClosestToGoal = 300;
        
        for (int a = 0; a < 8; a++)
        {
            PossibleDirections.Add(0);
            DirectionOfGoal.Add(0);
            InputData.Add("ground_check_" + a, 0);
            InputData.Add("goal_direction_" + a, 0);

        }

        // here we add a new check in the feedback that tells the agent if it has died yet

        InputData.Add("reset_agent", 0);
        InputData.Add("agent_closer", 0);
        InputData.Add("AgentDistance", 0);



        // here we add all the vectors to a list

        rayCastingPositions.Add(new Vector3(1f, -2.5f, 0f));
        rayCastingPositions.Add(new Vector3(1f, -2.5f, 1f));
        rayCastingPositions.Add(new Vector3(1f, -2.5f, -1f));
        rayCastingPositions.Add(new Vector3(-1f, -2.5f, 0f));
        rayCastingPositions.Add(new Vector3(-1f, -2.5f, 1f));
        rayCastingPositions.Add(new Vector3(-1f, -2.5f, -1f));
        rayCastingPositions.Add(new Vector3(0f, -2.5f, 1f));
        rayCastingPositions.Add(new Vector3(0f, -2.5f, -1f));

        
    }


    // Update is called once per frame
    void Update()
    {

        var reference_movement_instructions = evntmanager.GetComponent<ClientSocket>().TestSampleData;

        if (actualREset)
        {
            //print("RESETTING PLAYER");
            this.transform.position = new Vector3(0, 1, 0);
            reference_movement_instructions[4] = 0;
            ClosestToGoal = 30f;
            actualREset = false;
        }

        // check if we need to reset position due to max moves reached
        if(reference_movement_instructions[4] == 1)
        {
            actualREset = true;
            
        }

        // here we do checks to move the player agent
        if (reference_movement_instructions[0] == 1)
        {
            //print("move agent forward");
            this.transform.position = new Vector3(this.transform.position.x + 1f, this.transform.position.y, this.transform.position.z);
            reference_movement_instructions[0] = 0;
        }
        if (reference_movement_instructions[1] == 1)
        {
            //print("move agent backward");
            this.transform.position = new Vector3(this.transform.position.x - 1f, this.transform.position.y, this.transform.position.z);
            reference_movement_instructions[1] = 0;
        }
        if (reference_movement_instructions[2] == 1)
        {
            //print("move agent right");
            this.transform.position = new Vector3(this.transform.position.x, this.transform.position.y, this.transform.position.z - 1f);
            reference_movement_instructions[2] = 0;
        }
        if (reference_movement_instructions[3] == 1)
        {
            //print("move agent left");
            this.transform.position = new Vector3(this.transform.position.x, this.transform.position.y, this.transform.position.z + 1f);
            reference_movement_instructions[3] = 0;
        }

        // draw a line from agent towards its current goal
        Debug.DrawRay(transform.position, new Vector3(Goal.transform.position.x- transform.position.x, Goal.transform.position.y- transform.position.y, Goal.transform.position.z- transform.position.z), Color.green);

        if (Input.GetKeyDown("space"))
        {
            transform.position = transform.position + transform.forward;
        }

        // do some raycasting to detect ground around Agent
        RaycastHit hit;
        for (int i = 0; i < rayCastingPositions.Count; i++)
        {
            PossibleDirections[i] = 0;
            InputData["ground_check_" + i] = 0;
            //InputData["goal_direction_" + i] = 0;
            if (Physics.Raycast(new Vector3(transform.position.x, 3f, transform.position.z), rayCastingPositions[i], out hit, 3f))
            {
                Debug.DrawRay(new Vector3(transform.position.x, 3f, transform.position.z), rayCastingPositions[i], Color.red);
                PossibleDirections[i] = 1;
                InputData["ground_check_" + i] = 1;
            }
        }
        var old_dist = 10000f;
        var closest_pos = new Vector3(0, 0, 0);
        // do some checks to see which side of the agent is closest towards the goal xD
        foreach (Vector3 t in rayCastingPositions)
        {
            float dist = Vector3.Distance(t, new Vector3(Goal.transform.position.x - transform.position.x, Goal.transform.position.y - transform.position.y, Goal.transform.position.z - transform.position.z));
            if(dist< old_dist)
            {
                old_dist = dist;
                closest_pos = t;
            }
        }

        // now that we have the closest one, we can color it green
        Debug.DrawRay(new Vector3(transform.position.x, 3f, transform.position.z), closest_pos, Color.green);

        for (int c = 0; c < DirectionOfGoal.Count; c++)
        {
            DirectionOfGoal[c] = 0;
            InputData["goal_direction_" + c] = 0;
        }

        DirectionOfGoal[rayCastingPositions.IndexOf(closest_pos)] = 1;
        InputData["goal_direction_" + rayCastingPositions.IndexOf(closest_pos)] = 1;

        // here we check if we have moved closer to the goal, and if so then we reward the agent
        float moved_dist = Vector3.Distance(transform.position, new Vector3(Goal.transform.position.x - transform.position.x, Goal.transform.position.y - transform.position.y, Goal.transform.position.z - transform.position.z));

        //print("DISTANCE " + moved_dist);
        //print("DISTANCE GOAL" + ClosestToGoal);
        InputData["AgentDistance"] = (int)moved_dist;
        if (moved_dist < ClosestToGoal)
        {
            //update it and reward agent
            ClosestToGoal = moved_dist;
            //print("DISTANCE SCORE " + moved_dist);
            InputData["agent_closer"] = 1;
            

        }

        // check if ground beneith otherwise kill agent
        if (!Physics.Raycast(new Vector3(transform.position.x, 3f, transform.position.z), Vector3.down, out hit, 10f))
        {
            // here the agent has died, reset it
            InputData["reset_agent"] = 1;
            this.transform.position = new Vector3(0, 1, 0);
            reference_movement_instructions[4] = 0;
            ClosestToGoal = 30f;
        }


        // once move is over, we init the agent to do the next tick
        if (evntmanager.GetComponent<ClientSocket>().IsSwitch)
        {
            evntmanager.GetComponent<ClientSocket>().IsSwitch = false;
            // here we init the message to be sent back
            evntmanager.GetComponent<ClientSocket>().SendMessage();
        }
        


    }


}
