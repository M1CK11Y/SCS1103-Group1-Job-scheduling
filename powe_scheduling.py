
import time


load_shedding_timeline = {
    1: [0, 2],
    2: [2, 4],
    3: [4, 6],
    4: [6, 8],
    5: [8, 10],
    6: [10, 12],
    7: [12, 14],
    8: [14, 16],
    9: [16, 18],
    10: [18, 20],
    11: [20, 22],
    12: [22, 24],
}

#########################################################################################################################

class house():
    def __init__(self, area=any in load_shedding_timeline,units=5000, coocker=[0,5],sockets=[0,3],lights=[0,1],fridge=3):
        self.area=area
        self.units = units
        self.coocker = coocker
        self.sockets = sockets
        self.lights = lights
        self.fridge = fridge
        self.coocker_units=75
        self.socket_units=50


    def get_units(self):
        return self.units

    # --------------------------for coocker:---------------------------------------------------------------------------#

    def get_coocker(self):
        return self.coocker[0] * self.coocker[1]
    
    
    def use_coocker(self,hour):
        units = self.coocker[0] * self.coocker[1]
        if load_shedding_timeline[self.area][0]<=hour<load_shedding_timeline[self.area][1] and self.coocker[0]==0:
            print("CANT USE ON COOCKER")
        else:
            if units>0 and self.coocker_units >= units:
                self.coocker_units -= units
                return units

            if self.coocker_units -self.coocker[1]<= 0:
                self.coocker[0] = 0
                self.coocker_units=0
                print("Cooker automatically switched off.Usage limit reached")
                return 0


        return 0

    def set_coocker(self):
        if self.coocker[0]==0 and self.coocker_units >0:  # Ensuring coocker can only be turned on while set units are available
            self.coocker[0]=1

        elif self.coocker[0]==1:
            self.coocker[0]=0

        else:
            print("Coocker has already been used for 3 hours today. Please wait until tomorrow to use it again.")

    #-------------------------------for sockets----------------------------------------------------#

    
    def set_sockets(self):
        if self.sockets[0]==1:
            self.sockets[0]=0
        elif self.sockets[0]==0 and self.socket_units>0:
            self.sockets[0]=1
        else:
            print("You have used available units for sockets :( better luck next time ")

    def get_sockets(self):
        return self.sockets[0]*self.sockets[1]

    def use_sockets(self,hour):
        if load_shedding_timeline[self.area][0]<=hour<load_shedding_timeline[self.area][1] and self.sockets[0]==0:
            print("CANT USE SOCKETS")
        else:
            if self.socket_units - self.sockets[1]>=0:
                self.socket_units-=(self.sockets[1]*self.sockets[0])
                return self.sockets[1]*self.sockets[0]
            else:
                self.sockets[0]=0
                self.socket_units=0
                print("Socket usage limit reached")
                return 0
        return 0

    #--------------------------------for lights & Fridge-------------------------------------------#

    def set_lights(self,hour):
        if self.lights[0]==1:
            self.lights[0]=0
        else:
            if hour >= 18 or hour < 6:
                self.lights[0]=1
            else:
                print("Lights can only be turned on between 6 PM and 6 AM")

    def get_lights(self):
        return self.lights[1]*self.lights[0]

    def get_fridge(self):
        return self.fridge
    
    #---------------------------Editing units------------------------------------------------------#

    def add_units(self, newunits):
        self.units += newunits

    def use_units(self,hour,units):
        if load_shedding_timeline[self.area][0]<=hour<load_shedding_timeline[self.area][1]:
            print("DURING ZESA LOAD SHEDDING")
        else:
            required=units+self.get_fridge()
            if self.get_units() < required:
                print(f"Not enough units to perform Job. Required: {units}, Available: {self.get_units()}")
                

            else:
                print(f"Job requires: {units}, Available: {self.get_units()} Job successfully executed")
                self.add_units(-required) #always keep refridgerator on

###########################End of class############################################################

def use_house_units(myhouse,hour):
    
            
            print("Choose an option:  ")
            print("1. Turn on/off the coocker")
            print("2. Turn on/off the sockets")
            print("3. Turn on/off the lights")
            choice = input("Enter your choice a list of what you want to do in format ===>  1,2,3: ")

            if not choice.strip():
                print("No choice made.")
                return

            
            job_q = [int(x) for x in choice.strip().split(',') if x.strip().isdigit()]
            if len(job_q) == 0:
                print("No valid choices made.")
                return

            for job in job_q:
                if job == 1:
                    myhouse.set_coocker()
                elif job == 2:
                    myhouse.set_sockets()
                elif job == 3:
                    myhouse.set_lights(hour)
                else:
                    print(f"Invalid choice: {job}. Please choose 1, 2, or 3.")




def build_priority_list(myhouse,hour):
    joblist = ['fridge','coocker','sockets','lights']
    prioritylist = ['fridge']
    if hour >= 18 or hour < 6:
        prioritylist.append('lights')
    if myhouse.coocker_units>0 :
        if myhouse.get_units() >= myhouse.coocker[1]*3:
            prioritylist.append('coocker')
    if myhouse.get_units() > myhouse.sockets[1]*5:
        prioritylist.append('sockets')

    prioritylist+= [j for j in joblist if j not in prioritylist]

    return prioritylist


def priority_sort(arrA,arrB):
    n = len(arrA)
    sorted_arr = arrA.copy()

    for i in range(len(sorted_arr)):
        swapped=False
        for j in range(0, n - i - 1):
            left = arrB.index(sorted_arr[j]) if sorted_arr[j] in arrB else len(arrB)
            right = arrB.index(sorted_arr[j + 1]) if sorted_arr[j + 1] in arrB else len(arrB)
            if (left) > right:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped=True
        if not swapped:
            break

    return sorted_arr


def main(thehouse):


    limit =thehouse.get_units()//25
    warning=thehouse.get_units()//10
    
    for hour in range(24):
        print(f"ENTERING HOUR {hour}")

        units = thehouse.get_units()

        if units<=0:
            print("YOU EXHAUSTED ALL UNITS:")
            print("HAAA USUBHOWA KEMANGE.... MUKOMA MANYANYA ... YOU ARE OFFICIALLY CUT OFF ")
            print(f"YOU WERE CUT OF WITH {24-hour} hours in the day remaining ")
            print(f"zvinoita nature  bba marambidzwa kuramba muchitambisa magetsi")
            break

        elif units > limit:
            use_house_units(thehouse,hour)

        elif units >= warning:
            print("CRITICAL UNITS ARE LOW")

            additional_units=input("DO  YOU WISH TO ADD NEW UNITS input either 'y' for yes or 'n' for no").lower().strip()
            
            if additional_units=="y":
                    try:
                        addunits=float(input("ENTER UNITS BOUGHT").strip())
                        thehouse.add_units(addunits)

                    except ValueError:
                        print("CLEARLY BECAUSE THATS NOT A NUMBER ..... UNONYEPA... USUDELELA")


            else:
                print(f"WARNING: {units} units left")

                print("JOBS ARE: Coocker,lights,sockets (when inputing job list enter as is and separate jobs with ',')")
                pendingJobs=input("ENTER JOBS: ").lower().strip().split(',')

                for job in priority_sort(pendingJobs,build_priority_list(thehouse,hour)):
                    if job=="coocker":
                        thehouse.set_coocker()
                    elif job=="lights":
                        thehouse.set_lights(hour)

                    elif job=="sockets":
                        thehouse.set_sockets()

        power_used = (thehouse.use_coocker(hour)+ thehouse.use_sockets(hour)+ thehouse.get_lights())
        thehouse.use_units(hour,power_used)


        time.sleep(6.0)#simulates one seccond as ten minutes (this is 60 minutes)


newhouse = house(
    area=1,
    units=500,
    coocker=[0, 3],
    sockets=[0, 2],
    lights=[0, 1],
    fridge=3,
)

if __name__=="__main__":
    main(newhouse)
