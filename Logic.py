import datetime
import statistics

class PID:
    """
    Discrete PID control
    """

    def __init__(self, P=1.0, I=1.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator=Derivator
        self.Integrator=Integrator
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min

        self.set_point=0.0
        self.error=0.0

    def update(self,current_value):
        """
        Calculate PID output value for given reference input and feedback
        """

        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.I_value = self.Integrator * self.Ki

        PID = self.P_value + self.I_value + self.D_value

        return PID

    def setPoint(self,set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point = set_point
        self.Integrator=0
        self.Derivator=0

    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self,P):
        self.Kp=P

    def setKi(self,I):
        self.Ki=I

    def setKd(self,D):
        self.Kd=D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):
        return self.Derivator
    
    
    
class DataLogger:
    def __init__(self):
        pass
    
class Recipe:
    def __init__(self, strike_temp, sparge_temp, mash_temp, mash_time, boil_temp, boil_time):
        self.hlt = Keg(strike_temp)
        self.mash = Keg(mash_temp, mash_time)
        self.boil = Keg(boil_temp, boil_time)
        self.sparge_temp = sparge_temp
        self.steps = {1:self.hlt, 2:self.mash, 3:self.hlt, 4:self.boil}
        self.currentStep = 1
        self.keg = self.steps[1]
        self.run_time = self.mash.setTime + self.boil.setTime
        self.strike_volume = 5
        self.sparge_volume = 5
        self.done = False
        self.change = True
        self.controller = PID()
        self.controller.setPoint(self.keg.setTemp)
        self.tempLog = []
        self.start_step(1)
        
   
    def start_step(self, step):
        keg = self.steps[step]
        keg.start_time = datetime.datetime.now()
        keg.running = True
        
    def checkTime(self, keg):
        now = datetime.datetime.now()
        time = now - keg.start_time
        min_total = time.seconds/60
        min_left = keg.setTime - min_total
        return min_left
    
    def update(self):
        pidValue = self.controller.update(self.keg.temp)
        self.keg.temp = self.keg.temp + pidValue/28 #temp
        self.change = False
        if not(self.keg.stable):
            self.tempLog.append(self.keg.temp)
            self.tempLog = self.tempLog[-100:]
            if len(self.tempLog) == 100:
                stdev = statistics.stdev(self.tempLog)
                if stdev < 1.0:
                    self.keg.stable = True
        elif self.keg.time <= 0:
            self.keg.running = False
            self.currentStep+=1
            if self.currentStep == 5:
                self.done = True
            else:
                self.change = True
                self.keg = self.steps[self.currentStep]
                self.start_step(self.currentStep)
                self.controller.setPoint(self.keg.setTemp)
            if self.currentStep == 3:
                self.keg.setTemp = self.sparge_temp
        else:
            self.keg.time = self.checkTime(self.keg)
            
class Keg:
    def __init__(self, setTemp, setTime=0):
        self.temp = 55
        self.volume = 6
        self.setTemp = setTemp
        self.setTime = setTime
        self.running = False
        self.element_on = False
        self.stable = False
        self.time = setTime
        
