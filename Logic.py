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
    
class Controls:
    def __init__(self):
        self.hlt = Keg()
        self.mash = Keg()
        self.boil = Keg()
        self.steps = {1:self.hlt, 2:self.mash, 3:self.hlt, 4:self.boil}
        self.currentStep = 1
        self.keg = self.steps[1]
        self.done = False
        self.change = True
        self.controller = PID()
        self.start_step(1)
        self.time = datetime.datetime.now()
        self.started = False
        
   
    def start_step(self, step):
        keg = self.steps[step]
        self.tempLog = []
        keg.stable = False
        keg.running = True
        
    def checkTime(self, keg):
        now = datetime.datetime.now()
        time = now - keg.start_time
        min_total = time.seconds/60
        min_left = keg.setTime - min_total
        return min_left
    
    def update(self):
        self.change_temp()
        self.change = False
        if not(self.keg.stable):
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
                self.controller.setPoint(self.keg.setTemp)
                self.stupid_bit = True
            if self.currentStep == 3:
                self.keg.set_temp(self.recipe.sparge_temp)
        else:
            if self.stupid_bit:
                self.keg.start_time = datetime.datetime.now()
                self.stupid_bit = False
            self.keg.time = self.checkTime(self.keg)
            
    def change_temp(self):
        now = datetime.datetime.now()
        time = now - self.time
        if time.seconds >= 1 and self.started:
            pidValue = self.controller.update(self.keg.temp)
            self.keg.temp = self.keg.temp + pidValue/28 #temp
            self.tempLog.append(self.keg.temp)
            self.tempLog = self.tempLog[-100:]
            self.time = now
            
    def loadrecipe(self, strike_temp, sparge_temp, mash_temp, mash_time, boil_temp, boil_time):
        self.recipe = Recipe(strike_temp, sparge_temp, mash_temp, mash_time, boil_temp, boil_time)
        self.mash.set_temp(mash_temp)
        self.mash.set_time(mash_time)
        self.hlt.set_temp(strike_temp)
        self.boil.set_temp(boil_temp)
        self.boil.set_time(boil_time)
        self.controller.setPoint(self.keg.setTemp)
            
class Keg:
    def __init__(self):
        self.temp = 20
        self.volume = 0
        self.running = False
        self.element_on = False
        self.stable = False
        self.time = 0
        
    def set_temp(self, temp):
        self.setTemp = temp
    
    def set_time(self, time):
        self.setTime = time
        self.time = time
        
class Recipe:
    def __init__(self, strike_temp, sparge_temp, mash_temp, mash_time, boil_temp, boil_time):
        self.strike_temp = strike_temp
        self.mash_temp = mash_temp
        self.boil_temp = boil_temp
        self.mash_time = mash_time
        self.boil_time = boil_time
        self.sparge_temp = sparge_temp
        self.run_time = mash_time + boil_time       
        self.strike_volume = 5
        self.sparge_volume = 5

        
