from pymodbus.client import AsyncModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException
import asyncio

async def read_modbus_rtu():
    # User input for Modbus function, register address range, and serial port configuration
    modbus_function = input("Enter Modbus function (3 for Read Holding Registers[4x], 4 for Read Input Registers[3x]): ")
    start_address = int(input("Enter start address of register range: "))
    quantity = int(input("Enter quantity of registers to read: "))
    port_name = input("Enter serial port name (e.g., COM3, /dev/ttyUSB0): ")
    baud_rate = int(input("Enter baud rate (e.g., 9600): "))
    data_bits = int(input("Enter data bits (7 or 8): "))
    parity = input("Enter parity (N for None, E for Even, O for Odd): ")
    stop_bits = int(input("Enter stop bits (1 or 2):"))
    slave_id = int(input("Enter slave device ID: "))  # Prompt for slave device ID
    timeout = int(input("Enter timeout (1 for 1000 ms) "))

    # Setup Modbus RTU client
    client = ModbusClient(method='rtu',
                          port=port_name,
                          baudrate=baud_rate,
                          timeout=timeout,
                          parity=parity,
                          bytesize=data_bits,
                          stopbits=stop_bits)
    
    try:
         # Attempt to connect with a timeout of 30 seconds
        await asyncio.wait_for(client.connect(), timeout=30)
    except asyncio.TimeoutError:
        print("Connection attempt timed out after 30 seconds.")
        return
    except Exception as e:
        print(f"Failed to connect due to an error: {e}")
        return
    
    try:
        # Read registers based on user input
        if modbus_function == '3':
            response = client.read_holding_registers(address=start_address, count=quantity, slave=slave_id)
        elif modbus_function == '4':
            response = client.read_input_registers(address=start_address, count=quantity, slave=slave_id)
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
    asyncio.run(read_modbus_rtu())