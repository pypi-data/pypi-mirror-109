from .util import *


class Command:
    resolution_mode = 0

    def __init__(self, type: PSDTypes):
        self.type = type

    """
    Zx - Initialize PSD/4, Assign Valve Output to Right
    Yx - Initialize PSD/4, Assign Valve Output to Left
    Wx - Initialize PSD/4, Configure for No Valve
    """
    def initialize(self, drive: str, value=0):
        cmd: str = ''
        if drive == 'Z' or drive == 'Y' or drive == 'W':
            cmd += drive
        else:
            print("Error! Incorrect drive!")
            cmd = 'cmdError'
            return cmd
        if (value == 1) or (value >= 10 and value <= 40):
            cmd += str(value)
        return cmd

    """
    R - Execute Command Buffer
    X - Execute Command Buffer from Beginning
    """
    def executeCommandBuffer(self, type='R'):
        cmd: str = ''
        if type == 'R' or type == 'X':
            cmd += type
        else:
            print("Error! Incorrect type!")
            cmd = 'cmdError'
        return cmd

    """
        Syringe Commands
    """

    # z - Set Counter Position
    def setCounterPosition(self):
        return 'z'

    # Ax - Absolute Position
    def absolutePosition(self, value):
        cmd: str = 'A'
        cmd += str(value)
        return cmd

    # Px - Relative Pickup
    def relativePickup(self, value: int):
        cmd: str = 'P'
        cmd += str(value)
        return cmd

    # Dx - Relative Dispense
    def relativeDispense(self, value: int):
        cmd: str = 'D'
        cmd += str(value)
        return cmd

    # Kx - Return Steps
    def returnSteps(self, value: int):
        cmd: str = 'K'
        cmd += str(value)
        return cmd

    # kx - Back-off Steps
    def backoffSteps(self, value: int):
        cmd: str = 'k'
        cmd += str(value)
        return cmd

    '''
        Valve Commands
    '''

    # Ix - Move Valve to Input Position
    def moveValveToInputPosition(self, value=0):
        cmd: str = 'I'
        if value == 0:
            pass
        elif 1 <= value <= 8:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Move valve to input position command!")
            cmd = 'cmdError'
        return cmd

    # Ox - Move Valve to Output Position
    def moveValveToOutputPosition(self, value=0):
        cmd: str = 'O'
        if value == 0:
            pass
        elif 1 <= value <= 8:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Move valve to output position command!")
            cmd = 'cmdError'
        return cmd

    # B - Move Valve to Bypass (Throughput Position)
    def moveValveToBypass(self):
        return 'B'

    # E - Move Valve to Extra Position
    def moveValveToExtraPosition(self):
        return 'E'

    """
        Action commands
    """

    # g - Define a Position in a Command String
    def definePositionInCommandString(self):
        return 'g'

    # Gx - Repeat Commands
    def repeatCommands(self, value=0):
        cmd: str = 'G'
        if value == 0:
            pass
        elif 1 <= value <= 65535:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Repeat Commands command!")
            cmd = 'cmdError'
        return cmd

    # Mx - Delay - performs a delay of x milliseconds.where 5 ≤ x ≤ 30,000 milliseconds.
    def delay(self, value: int):
        cmd: str = 'M'
        if 5 <= value <= 30000:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Delay command!")
            cmd = 'cmdError'
        return cmd

    # Hx - Halt Command Execution
    def halt(self, value: int):
        cmd: str = 'H'
        if 0 <= value <= 2:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Halt command!")
            cmd = 'cmdError'
        return cmd

    # Jx - Auxiliary Outputs
    def auxiliaryOutputs(self, value: int):
        cmd: str = 'J'
        if 0 <= value <= 7:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Auxiliary Outputs command!")
            cmd = 'cmdError'
        return cmd

    # sx - Store Command String
    def storeCommandString(self, location: int, command: str):
        cmd: str = 's'
        if 0 <= location <= 14:
            cmd += str(location)
            cmd += command
        else:
            print("Invalid value " + str(location) + " for Store Command String command!")
            cmd = 'cmdError'
        return cmd

    # ex - Execute Command String in EEPROM Location
    def executeCommandStringInEEPROMLocation(self, location: int):
        cmd: str = 'e'
        if 0 <= location <= 14:
            cmd += str(location)
        else:
            print("Invalid value " + str(location) + " for Execute Command String in EEPROM Location command!")
            cmd = 'cmdError'
        return cmd

    def terminateCommandBuffer(self):
        return 'T'

    """
        Motor Commands
    """

    def setAcceleration(self, value: int):
        cmd: str = 'L'
        if 0 <= value <= 20:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Set acceleration command!")
            cmd = 'cmdError'
        return cmd

    def setSpeed(self, value: int):
        cmd: str = 'S'
        if 1 <= value <= 40:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Set speed command!")
            cmd = 'cmdError'
        return cmd

    def increaseStopVelocityBySteps(self, value: int):
        cmd: str = 'C'
        if 0 <= value <= 25:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Increase Stop Velocity by Steps command!")
            cmd = 'cmdError'
        return cmd

    def setStartVelocity(self, value: int):
        cmd: str = 'v'
        if 50 <= value <= 1000:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Set start velocity command!")
            cmd = 'cmdError'
        return cmd

    def setMaximumVelocity(self, value: int):
        cmd: str = 'V'
        if 2 <= value <= 5800:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Set maximum velocity command!")
            cmd = 'cmdError'
        return cmd

    def stopVelocity(self, value: int):
        cmd: str = 'c'
        if 50 <= value <= 2700:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for Stop velocity command!")
            cmd = 'cmdError'
        return cmd

    """
        h30001 - Enable h Factor Commands and Queries
        h30000 - Disable h Factor Commands and Queries
    """

    def enableHFactorCommandsAndQueries(self):
        return "h30001"

    def disableHFactorCommandsAndQueries(self):
        return "h30000"

    def resetPSD(self):
        return "h30003"

    def initializeValve(self):
        return "h20000"

    def initializeSyringeOnly(self, speedCode: int):
        cmd: str = 'h'
        cmdValue = 10000
        # permitted values between 0-40
        if 0 <= speedCode <= 40:
            cmdValue += speedCode
            cmd += str(cmdValue)
        else:
            print("Invalid speed code " + str(speedCode) + " for Initialize Syringe Only command!")
            cmd = 'cmdError'
        return cmd

    def setSyringeMode(self, mode: int):
        cmd: str = 'h'
        cmdValue = 11000
        # permitted values between 0-15
        if 0 <= mode <= 15:
            cmdValue += mode
            cmd += str(cmdValue)
        else:
            print("Invalid mode " + str(mode) + " for Set Syringe Mode command!")
            cmd = 'cmdError'
        return cmd

    def enableValveMovement(self):
        return "h20001"

    def disableValveMovement(self):
        return "h20002"

    def setValveType(self, type: int):
        cmd: str = 'h2100'
        # permitted values between 0-6
        if 0 <= type <= 6:
            cmd += str(type)
        else:
            print("Invalid valve type " + str(type) + " for Set Valve Type command!")
            cmd = 'cmdError'
        return cmd

    def moveValveToInputPositionInShortestDirection(self):
        return "h23001"

    def moveValveToOutputPositionInShortestDirection(self):
        return "h23002"

    def moveValveToWashPositionInShortestDirection(self):
        return "h23003"

    def moveValveToReturnPositionInShortestDirection(self):
        return "h23004"

    def moveValveToBypassPositionInShortestDirection(self):
        return "h23005"

    def moveValveToExtraPositionInShortestDirection(self):
        return "h23006"

    def moveValveClockwiseDirection(self, position: int):
        cmd: str = 'h2400'
        # permitted values between 1-8
        if 1 <= position <= 8:
            cmd += str(position)
        else:
            print("Invalid position " + str(position) + " for Move Valve in Clockwise Direction command!")
            cmd = 'cmdError'
        return cmd

    def moveValveCounterclockwiseDirection(self, position: int):
        cmd: str = 'h2500'
        # permitted values between 1-8
        if 1 <= position <= 8:
            cmd += str(position)
        else:
            print("Invalid position " + str(position) + " for Move Valve in Counterclockwise Direction command!")
            cmd = 'cmdError'
        return cmd

    def moveValveInShortestDirection(self, position: int):
        cmd: str = 'h2600'
        # permitted values between 1-8
        if 1 <= position <= 8:
            cmd += str(position)
        else:
            print("Invalid position " + str(position) + " for Move Valve in Shortest Direction command!")
            cmd = 'cmdError'
        return cmd

    def angularValveMoveCommandCtr(self, cmdValue: int, incrementWith: int):
        cmd: str = 'h'
        # permitted values between 0-345 incremented by 15
        if 345 >= incrementWith >= 0 == incrementWith % 15:
            cmdValue += incrementWith
            cmd += str(cmdValue)
        else:
            print("Invalid angle value " + str(incrementWith) + " for Angular Valve Move command!")
            cmd = 'cmdError'
        return cmd

    def clockwiseAngularValveMove(self, position: int):
        return self.angularValveMoveCommandCtr(27000, position)

    def counterclockwiseAngularValveMove(self, position: int):
        return self.angularValveMoveCommandCtr(28000, position)

    def shortestDirectAngularValveMove(self, position: int):
        return self.angularValveMoveCommandCtr(29000, position)

    """
        Query Commands
    """

    def commandBufferStatusQuery(self):
        return QueryCommandsEnumeration.BUFFER_STATUS.value

    def pumpStatusQuery(self):
        return QueryCommandsEnumeration.PUMP_STATUS.value

    def absoluteSyringePosition(self):
        return QueryCommandsEnumeration.ABSOLUTE_SYRINGE_POSITION.value

    def firmwareVersionQuery(self):
        return QueryCommandsEnumeration.FIRMWARE_VERSION.value

    def firmwareChecksumQuery(self):
        return QueryCommandsEnumeration.FIRMWARE_CHECKSUM.value

    def startVelocityQuery(self):
        return QueryCommandsEnumeration.START_VELOCITY.value

    def maximumVelocityQuery(self):
        return QueryCommandsEnumeration.MAXIMUM_VELOCITY.value

    def stopVelocityQuery(self):
        return QueryCommandsEnumeration.STOP_VELOCITY.value

    def actualPositionOfSyringeQuery(self):
        return QueryCommandsEnumeration.ACTUAL_SYRINGE_POSITION.value

    def numberOfReturnStepsQuery(self):
        return QueryCommandsEnumeration.NUMBER_OF_RETURN_STEPS.value

    def statusOfAuxiliaryInput1Query(self):
        return QueryCommandsEnumeration.STATUS_AUXILIARY_INPUT_1.value

    def statusOfAuxiliaryInput2Query(self):
        return QueryCommandsEnumeration.STATUS_AUXILIARY_INPUT_2.value

    def returns255Query(self):
        return QueryCommandsEnumeration.RETURNS_255.value

    def numberOfBackoffStepsQuery(self):
        return QueryCommandsEnumeration.NUMBER_OF_BACKOFF_STEPS.value

    def syringeStatusQuery(self):
        return QueryCommandsEnumeration.SYRINGE_STATUS.value

    def syringeModeQuery(self):
        return QueryCommandsEnumeration.SYRINGE_MODE.value

    def valveStatusQuery(self):
        return QueryCommandsEnumeration.VALVE_STATUS.value

    def valveTypeQuery(self):
        return QueryCommandsEnumeration.VALVE_TYPE.value

    def valveLogicalPositionQuery(self):
        return QueryCommandsEnumeration.VALVE_LOGICAL_POSITION.value

    def valveNumericalPositionQuery(self):
        return QueryCommandsEnumeration.VALVE_NUMERICAL_POSITION.value

    def valveAngleQuery(self):
        return QueryCommandsEnumeration.VALVE_ANGLE.value

    def lastDigitalOutValueQuery(self):
        return QueryCommandsEnumeration.LAST_DIGITAL_OUT_VALUE.value