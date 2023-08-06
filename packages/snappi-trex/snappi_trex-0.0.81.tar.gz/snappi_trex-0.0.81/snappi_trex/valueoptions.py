from trex.stl.api import *


class ValueOptions:
    """
    This class contains the method to configure header field variables.
    This class also contains useful utility functions for configuration
    """

    def get_value_cmds(layer_type, layer_cnt, header_field, length, field_str, fixup=0):
        """
        Returns the set of VM instructions to configure a specific header field
        to a value option. 
        args:
            - layer_type: A string representing the header type (Must conform to Scapy protocol types)
            - layer_cnt: An int representing the number of occurrences of 
                        this layer type in the packet base
            - header_field: A dictionary object that contains the value configuration 
                        information for the given header field
            - length: An int representing the length of the header field in bits
            - field_str: A string representing the field (Must conform to Scapy protocol fields)
            - fixup: An int representing how many packet bytes to go forward when writing the field bytes.
                        (Positive fixup means forward, negative means backward)
        """
        varname = "{0}{1}_{2}".format(layer_type, layer_cnt-1, field_str)
        vm_cmds = []
        mask = ValueOptions.get_mask(length)

        # If length is more than 4 bytes, call get_big_value_cmds
        if length > 32:
            return ValueOptions.get_big_value_cmds(
                layer_type, layer_cnt, header_field, length, field_str, fixup
            )
        
        elif length > 16:
            numBytes = 4
        elif length > 8:
            numBytes = 2
        else:
            numBytes = 1

        # Handle every source port value option: Value, values, inc, dec
        if header_field['choice'] == 'value':
            add_val = 0
            val = ValueOptions.convert_to_long(header_field['value'], layer_type)
            vm_cmds.append(STLVmFlowVar(name=varname, size=numBytes,
                min_value=val, max_value=val, step=1, op='inc'
            ))

        elif header_field['choice'] == 'values':
            add_val = 0
            value_list = []
            for v in header_field['values']:
                value_list.append(ValueOptions.convert_to_long(v, layer_type))
            vm_cmds.append(STLVmFlowVar(name=varname, size=numBytes,
                value_list=value_list
            ))

        elif header_field['choice'] == 'increment':
            start = ValueOptions.convert_to_long(header_field['increment']['start'], layer_type)
            step = ValueOptions.convert_to_long(header_field['increment']['step'], layer_type)
            cnt = header_field['increment']['count']
            minV, maxV, init, add_val = ValueOptions.inc_values(start,step,cnt,length)
            vm_cmds.append(STLVmFlowVar(name=varname, size=numBytes, init_value = init,
                min_value=minV, max_value=maxV, step=step, op='inc'
            ))

        elif header_field['choice'] == 'decrement':
            start = ValueOptions.convert_to_long(header_field['decrement']['start'], layer_type)
            step = ValueOptions.convert_to_long(header_field['decrement']['step'], layer_type)
            cnt = header_field['decrement']['count']
            minV, maxV, init, add_val = ValueOptions.inc_values(start,-step,cnt,length)
            vm_cmds.append(STLVmFlowVar(name=varname, size=numBytes, init_value = init,
                min_value=minV, max_value=maxV, step=step, op='dec'
            ))

        else: 
            raise STLError('Invalid {0} operation'.format(varname))
        
        # Write the first n bits of the variable to the first n bits of the packet field
        pkt_offset = "{0}:{1}.{2}".format(layer_type, layer_cnt-1, field_str)
        bit_shift = numBytes*8-length
        add_val_int = ValueOptions.uint_to_int(add_val, 32)
        vm_cmds.append(STLVmWrMaskFlowVar(fv_name=varname, 
                                    pkt_cast_size=numBytes,
                                    mask=mask << bit_shift,
                                    shift = bit_shift,
                                    pkt_offset=pkt_offset, 
                                    offset_fixup=fixup,
                                    add_value=add_val_int))
        
        return vm_cmds


    def get_big_value_cmds(layer_type, layer_cnt, header_field, length, field_str, fixup):
        """
        Same as get_value_cmds (see above). Handles fields of size 33-64 inclusive
        """
        varname = "{0}{1}_{2}".format(layer_type, layer_cnt-1, field_str)
        vm_cmds = []
        mask = ValueOptions.get_mask(length) 

        # Handle every source port value option: Value, values, inc, dec
        if header_field['choice'] == 'value':
            add_val = 0
            val = ValueOptions.convert_to_long(header_field['value'], layer_type)
            vm_cmds.append(STLVmFlowVar(name=varname, size=8,
                min_value=val, max_value=val, step=1, op='inc'
            ))

        elif header_field['choice'] == 'values':
            add_val = 0
            value_list = []
            for v in header_field['values']:
                value_list.append(ValueOptions.convert_to_long(v, layer_type))

            vm_cmds.append(STLVmFlowVar(name=varname, size=8,
                value_list=value_list
            ))

        elif header_field['choice'] == 'increment':
            start = ValueOptions.convert_to_long(header_field['increment']['start'], layer_type)
            step = ValueOptions.convert_to_long(header_field['increment']['step'], layer_type)
            cnt = header_field['increment']['count']
            minV, maxV, init, add_val = ValueOptions.inc_values(start,step,cnt,length)
            
            vm_cmds.append(STLVmFlowVar(name=varname, size=8, init_value = init,
                min_value=minV, max_value=maxV, step=step, op='inc'
            ))

        elif header_field['choice'] == 'decrement':
            start = ValueOptions.convert_to_long(header_field['decrement']['start'], layer_type)
            step = ValueOptions.convert_to_long(header_field['decrement']['step'], layer_type)
            cnt = header_field['decrement']['count']
            minV, maxV, init, add_val = ValueOptions.inc_values(start,-step,cnt,length)
            
            vm_cmds.append(STLVmFlowVar(name=varname, size=8, init_value = init,
                min_value=minV, max_value=maxV, step=step, op='dec'
            ))

        else: 
            raise STLError('Invalid {0} operation'.format(varname))
        
        pkt_offset = "{0}:{1}.{2}".format(layer_type, layer_cnt-1, field_str)
        bit_shift = 64-length
        bit_mask = mask >> 32 << bit_shift

        # Write first n-32 bits of data
        add_val_top = ValueOptions.uint_to_int(add_val>>32, 32)
        vm_cmds.append(STLVmWrMaskFlowVar(fv_name=varname, 
                                pkt_cast_size=4,
                                mask=bit_mask,
                                shift = bit_shift,
                                pkt_offset=pkt_offset, 
                                offset_fixup=fixup,
                                add_value=add_val_top))

        # Write last 4 bytes
        num_bytes = (length+7)//8
        add_val_bot = ValueOptions.uint_to_int(add_val, 32)
        for i in range(3, -1, -1):
            vm_cmds.append(STLVmWrMaskFlowVar(fv_name=varname, 
                                    is_big=False,
                                    shift = -8*i,
                                    pkt_offset=pkt_offset, 
                                    offset_fixup=num_bytes-i-1,
                                    add_value=add_val_bot))

        return vm_cmds


    def inc_values(start, step, count, length):
        """
        Returns the min, max, initial, and add value for a given start, step, 
        count, and mask value for incrementing or decrementing fields. The min
        value is either the bottom value of the decrement or the initial value of
        the increment. The max value is either the top value of the increment or
        the initial value of the decrement. The add value is how much needs to be 
        added in order to correct the start value
        args:
            - start: int representing start value of the increment or decrement
            - step: int representing how much to increment or decrement by.
                    (Positive means increment, negative means decrement)
            - count: number of increments before cycling to the start
            - mask: a mask containing all 1's with a length of the field length
        """
        if abs(step) * count >= (1 << length):
            raise STLError('incrementing/decrementing count is too high.' + 
            'step*count must be at most {0} bits long'.format(length))

        if step < 0: # Decrementing
            step = -((-step) % (1<<length))
            max = init = ValueOptions.get_mask(length)
            min = max + count * step
            add_val = (start + 1) % (1<<length)

        else: # Incrementing
            step = step % (1<<length)
            min = init = 0
            max = min + count * step
            add_val = start
        
        return (min, max, init, add_val)


    def get_mask(bits):
        """
        returns a mask of 1's of size bits
        """
        result = (1 << bits) - 1
        return result

    
    def uint_to_int(uint, size):
        """
        converts an unsigned int of size n to a signed int of size n
        """
        result = uint & ValueOptions.get_mask(size)
        if result >= (1 << (size-1)):
            result -= (1 << size)
        return result


    def convert_to_long(value, layer_type):
        """
        Parses address values into a long int
        args:
            - value: A string or long representing the address
            - layer_type: A string representing the layer type
        """
        if isinstance(value, int): 
            return value

        if layer_type == 'IP':
            elements = value.split('.')
            result = 0
            for e in elements:
                result = result << 8
                if len(e) == 0:
                    continue
                result += int(e)
            return result

        if layer_type == 'Ethernet':
            elements = value.split(':')
            result = 0
            for e in elements:
                result = result << 8
                if len(e) == 0:
                    continue
                result += int(e, 16)
            return result
        
        return value