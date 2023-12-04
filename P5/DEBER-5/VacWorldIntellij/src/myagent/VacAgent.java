/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package myagent;

import agent.Action;
import agent.Agent;
import agent.Percept;
import vacworld.ShutOff;
import vacworld.SuckDirt;
import vacworld.TurnLeft;
import vacworld.TurnRight;
import vacworld.VacPercept;

/* Change the code as appropriate.  This code
   is here to help you understand the mechanism
   of the simulator. 
*/

public class VacAgent extends Agent {

    private final String ID = "1";
    // Think about locations you already visited.  Remember those.
    private boolean dirtStatus = true;
    private boolean bumpFeltInPrevMove = true;
    private boolean obstacleInFront = true;

    public void see(Percept p) {

        VacPercept vp = (VacPercept) p;
        dirtStatus = vp.seeDirt();
        bumpFeltInPrevMove = vp.feelBump();
        obstacleInFront = vp.seeObstacle();
    }

    public Action selectAction() {
        Action action = new SuckDirt();
        SuckDirt suckDirt = new SuckDirt();
        TurnLeft turnLeft = new TurnLeft();
        TurnRight turnRight = new TurnRight();
        ShutOff shutOff = new ShutOff();
        
        if(dirtStatus)
            action = suckDirt;
        if(bumpFeltInPrevMove)
              action = turnLeft;
        if(obstacleInFront)
              action = turnRight;
        
        return action;
    }

    public String getId() {
        return ID;
    }

}
