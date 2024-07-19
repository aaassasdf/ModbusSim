from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException

def read_modbus_rtu():
    # User input for Modbus function, register address range, and serial port configuration
    modbus_function = input("Enter Modbus function (3 for Read Holding Registers[4x], 4 for Read Input Registers[3x]): ")
    start_address = int(input("Enter start address of register range: "))
    quantity = int(input("Enter quantity of registers to read: "))
    port_name = input("Enter serial port name (e.g., COM3, /dev/ttyUSB0): ")
    baud_rate = int(input("Enter baud rate (e.g., 9600): "))

    # Setup Modbus RTU client
    client = ModbusClient(method='rtu', port=port_name, baudrate=baud_rate, timeout=1)
    connection = client.connect()

    if not connection:
        print("Failed to connect to the Modbus server.")
        return
    
    try:
        # Read registers based on user input
        if modbus_function == '3':
            response = client.read_holding_registers(address=start_address, count=quantity, unit=1)
        elif modbus_function == '4':
            response = client.read_input_registers(address=start_address, count=quantity, unit=1)
        else:
            print("Invalid Modbus function. Please enter 3 or 4.")
            return

        # Check for errors and print register values
        if not response.isError():
            print("Register values:", response.registers)
        else:
            print("Error reading registers:", response)

    except ModbusException as e:
        print("Modbus error:", e)
    finally:
        client.close()

if __name__ == "__main__":
    read_modbus_rtu()