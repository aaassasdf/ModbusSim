# Import necessary libraries
from pymodbus.server import StartSerialServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Define the main function to setup and run the Modbus RTU server
def run_modbus_rtu_server():
    # Configure the serial port settings
    port = 'COM11'  # Adjust this to the desired COM port on Windows
    baudrate = 9600  # Adjust baud rate as needed
    timeout = 1  # Timeout for the server in seconds

    # Create a block of memory to store data, initializing first 10 registers with zeros
    data = list()
    cnt = 0
    request_length = 10
    state = 0
    while cnt < request_length:
        print("Command:\n")
        print("exit - To exit the program")
        
        ipt = input(f"Enter the number to be stored in the register {cnt}: ")
        if ipt == "exit":
            break

        elif ipt in "0123456789":
            ipt = int(ipt)

        data.append(int(ipt))
        cnt += 1

    if len(data) < request_length:
        data.append( [0] * (request_length - len(data)))

    # Create a Modbus block and context to store the data
    block = ModbusSequentialDataBlock(0, data) # Address of the first register is 0
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block) # Store data in all four register types
    context = ModbusServerContext(slaves=store, single=True) # Create a single slave context

    # Setup server identity
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'PyModbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'PyModbus Server'
    identity.ModelName = 'PyModbus Server'
    identity.MajorMinorRevision = '1.0'

    # Start the Modbus RTU server
    StartSerialServer(context=context, identity=identity, port=port, baudrate=baudrate, timeout=timeout)

if __name__ == "__main__":
    run_modbus_rtu_server()