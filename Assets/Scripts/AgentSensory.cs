using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class AgentSensory : MonoBehaviour
{

    public GameObject Goal;

    public GameObject SELF;

    public bool actualREset = false;

    public List<GameObject> Ground_Front;
    public List<int> PossibleDirections;

    public List<int> DirectionOfGoal;

    public GameObject evntmanager;

    public Text goalDistance;
    public Text MaxgoalDistance;
    public Text goalDirection;
    public Text GoalRewardText;

    public bool GoalTraining = false;

    public Vector3 new_place3D;

    // here we have a json dict that has all the data we need for the server

    public Dictionary<string, int> InputData = new Dictionary<string, int>();

    public List<Vector3> rayCastingPositions;
    // Start is called before the first frame update


    // define a float to show the closest the agent has been to the goal in this life, and if it gets closer then update this and reward it
    public float ClosestToGoal = 30f;

    public List<float> angless;
    public List<Vector3> CircleCoordsToPlace;
    public int CircleDistance = 10;
    public int NumberOfPointsToCheck = 16;

    public float InitGoalDist = 21f;

    void Start()
    {
        ClosestToGoal = 300;
        CircleDistance = 1;
        NumberOfPointsToCheck = 16;

        InputData["init_goal"] = 21;

        for (int a = 0; a < NumberOfPointsToCheck; a++)
        {
            PossibleDirections.Add(0);
            DirectionOfGoal.Add(0);
            
            InputData.Add("gr" + a, 0);
            InputData.Add("gd" + a, 0);

        }

        print(DirectionOfGoal.Count);

        // here we add a new check in the feedback that tells the agent if it has died yet

        InputData.Add("reset_agent", 0);
        InputData.Add("agent_closer", 0);
        InputData.Add("AgentDistance", 0);

        


        // here generate 360 empty angles
        for (int i = 0; i < 360; i++)
        {
            angless.Add(0f);
            CircleCoordsToPlace.Add(new Vector3(0, 0, 0));
        }


    }


    // Update is called once per frame
    void Update()
    {

        

        // HERE WE UPDATE THE DEBUGGING TEXT ELEMENTS
        var dist_temp = Vector3.Distance(transform.position, new Vector3(Goal.transform.position.x, Goal.transform.position.y, Goal.transform.position.z));
        
        goalDistance.text = "Goal Dist = " + dist_temp;
        MaxgoalDistance.text = "Goal Dist = " + ClosestToGoal;
        GoalRewardText.text = "Reward = " + ((InitGoalDist - dist_temp)*10);

        // here we get the circle points
        for (int p = 0; p < NumberOfPointsToCheck; p++)
        {
            var angd = 360 / NumberOfPointsToCheck * p;
            angless[p] = angd;
            
        }

        for (int h = 0; h < angless.Count; h++)
        {
            // here we generate the 16 circle points 
            var centerr = new Vector2(transform.position.x, transform.position.z);
            var test_angle = angless[h];
            var ttttt = Mathf.Deg2Rad * test_angle;
            var coorddz = Mathf.Sin(ttttt) / CircleDistance;
            var coorddx = Mathf.Cos(ttttt) / CircleDistance;
            var new_place = new Vector2(centerr.x + coorddx, centerr.y + coorddz);
            var new_place3DD = new Vector3(new_place.x, transform.position.y, new_place.y);
            CircleCoordsToPlace[h] = new_place3DD;
            //print("" + h + ":" + new_place3DD);
        }

        var reference_movement_instructions = evntmanager.GetComponent<ClientSocket>().TestSampleData;

        // Here we check if the player is dying, and we reset its pos and randomize the goals position
        if (actualREset)
        {
            
            
            //print("RESETTING PLAYER");
            this.transform.position = new Vector3(0, 1, 0);
            reference_movement_instructions[4] = 0;

            // reset the call to reset the player due to falling off map
            InputData["reset_agent"] = 0;

            actualREset = false;
        }

        // check if we need to reset position due to max moves reached
        if(reference_movement_instructions[8] == 1)
        {
            actualREset = true;
            InputData["reset_agent"] = 0;

            // here we update and move the goal to a new position
            var new_goal_pos = new Vector3(Random.Range(-15.0f, 15.0f), 1, Random.Range(-15.0f, 15.0f));
            if (GoalTraining) {
                Goal.transform.position = new_goal_pos; // USE THIS IF TRAINING AGENT WHAT A GOAL IS, SO IT MOVES GOAL SPAWN EVERY LIFE
            }

            float actual_DISTANCE = Vector3.Distance(transform.position, new Vector3(Goal.transform.position.x - transform.position.x, Goal.transform.position.y - transform.position.y, Goal.transform.position.z - transform.position.z));
            ClosestToGoal = actual_DISTANCE; //30f
            // pass this distance from goal to the NN
            InputData["init_goal"] = (int)actual_DISTANCE;
            InitGoalDist = actual_DISTANCE;

        }

        // HERE ARE MOVEMENT INDEXES 

        // 0 forward
        // 1 backward
        // 2 left
        // 3 right
        // 4 reset game
        // 5 forward left
        // 6 forward right
        // 7 backward left
        // 8 backward right

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
            //print("move agent left");  left
            this.transform.position = new Vector3(this.transform.position.x, this.transform.position.y, this.transform.position.z + 1f);
            reference_movement_instructions[3] = 0;
        }
        if (reference_movement_instructions[4] == 1)
        {
            //print("move agent left"); forward left
            this.transform.position = new Vector3(this.transform.position.x + 1, this.transform.position.y, this.transform.position.z + 1f);
            reference_movement_instructions[4] = 0;
        }
        if (reference_movement_instructions[5] == 1)
        {
            //print("move agent left"); forward right
            this.transform.position = new Vector3(this.transform.position.x + 1, this.transform.position.y, this.transform.position.z - 1f);
            reference_movement_instructions[5] = 0;
        }
        if (reference_movement_instructions[6] == 1)
        {
            //print("move agent left");  backward left
            this.transform.position = new Vector3(this.transform.position.x - 1, this.transform.position.y, this.transform.position.z + 1f);
            reference_movement_instructions[6] = 0;
        }
        if (reference_movement_instructions[7] == 1)
        {
            //print("move agent left"); backward right
            this.transform.position = new Vector3(this.transform.position.x - 1, this.transform.position.y, this.transform.position.z - 1f);
            reference_movement_instructions[7] = 0;
        }

        // draw a line from agent towards its current goal
        Debug.DrawRay(transform.position, new Vector3(Goal.transform.position.x- transform.position.x, Goal.transform.position.y- transform.position.y, Goal.transform.position.z- transform.position.z), Color.green);

        // here we draw vertical lines by all the ground check positions
        for (int u = 0; u < NumberOfPointsToCheck; u++)
        {
            // draw a vertical line by the test coord to showcase lmafwaf
            Debug.DrawRay(CircleCoordsToPlace[u], Vector3.down, Color.cyan);
        }

        // testing manual movement
        if (Input.GetKeyDown("space"))
        {
            transform.position = transform.position + transform.forward;
        }

        // UPDATED METHOD
        // do some raycasting to detect ground around Agent
        RaycastHit hit;
        for (int i = 0; i < NumberOfPointsToCheck; i++)
        {
            PossibleDirections[i] = 0;
            InputData["gr" + i] = 0;
            if (Physics.Raycast(CircleCoordsToPlace[i], Vector3.down, out hit, 3f))
            {
                Debug.DrawRay(CircleCoordsToPlace[i], Vector3.down, Color.red);
                PossibleDirections[i] = 1;
                InputData["gr" + i] = 1;
            }
        }

        var old_dist = 10000f;
        var closest_pos = new Vector3(0, 0, 0);
        // do some checks to see which side of the agent is closest towards the goal xD
        foreach (Vector3 t in CircleCoordsToPlace)
        {
            float dist = Vector3.Distance(t, new Vector3(Goal.transform.position.x, Goal.transform.position.y, Goal.transform.position.z));
            if (dist < old_dist)
            {
                old_dist = dist;
                closest_pos = t;
            }
        }

        // now that we have the closest one, we can color it green
        Debug.DrawRay(closest_pos, Vector3.down, Color.yellow);

        for (int c = 0; c < DirectionOfGoal.Count; c++)
        {
            DirectionOfGoal[c] = 0;
            InputData["gd" + c] = 0;
        }

        // here we update the vars to reflect the closest check to the goal
        DirectionOfGoal[CircleCoordsToPlace.IndexOf(closest_pos)] = 1;
        InputData["gd" + CircleCoordsToPlace.IndexOf(closest_pos)] = 1;

        // here we check if we have moved closer to the goal, and if so then we reward the agent
        float moved_dist = Vector3.Distance(transform.position, new Vector3(Goal.transform.position.x - transform.position.x, Goal.transform.position.y - transform.position.y, Goal.transform.position.z - transform.position.z));

        // HERE WE UPDATE THE VARIABLES FOR THE DISTANCE FROM THE GOAL
        //InputData["AgentDistance"] = (int)moved_dist;
        if (moved_dist < ClosestToGoal)
        {
            //update it and reward agent
            ClosestToGoal = moved_dist;
            InputData["agent_closer"] = 1;
            InputData["AgentDistance"] = (int)moved_dist;


        }

        // check if ground beneith otherwise kill agent
        // bug where it hardlocks being reset, so we need to reset the reset value lol
        if (!Physics.Raycast(new Vector3(transform.position.x, 3f, transform.position.z), Vector3.down, out hit, 10f))
        {
            // here the agent has died, reset it
            InputData["reset_agent"] = 1;
            this.transform.position = new Vector3(0, 1, 0);
            reference_movement_instructions[4] = 0;
            ClosestToGoal = 30f;

            // here we update and move the goal to a new position
            var new_goal_pos = new Vector3(Random.Range(-15.0f, 15.0f), 1, Random.Range(-15.0f, 15.0f));
            if (GoalTraining)
            {
                Goal.transform.position = new_goal_pos; // ONLY USE THIS WHEN TRAINING AGENT TO MOVE TOWARDS GOALS
            }
                
                float actual_DISTANCE = Vector3.Distance(transform.position, new Vector3(Goal.transform.position.x - transform.position.x, Goal.transform.position.y - transform.position.y, Goal.transform.position.z - transform.position.z));
            ClosestToGoal = actual_DISTANCE; //30f
            // pass this distance from goal to the NN
            InputData["init_goal"] = (int)actual_DISTANCE;
            InitGoalDist = actual_DISTANCE;
        }
        else
        {
            // here there is ground below player, so we dont reset it
            InputData["reset_agent"] = 0;
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
