
### Find the points of verteces of the 2D profile of TF coil


def find_points(lower_inner_coordinates,mid_point_coordinates,thickness,test=False):
    """

    lower_inner_coordinates must be a 2 element tuple
    mid_point_coordinates must be a 2 elemenet tuple
    thickness must be a float or an int
    test=True will print the returned coordinates to console

    """

    ### Check if input values are what they meant to be ###
    if (tup_check(lower_inner_coordinates) or tup_check(mid_point_coordinates)) == False:
        print("Wrong Data type, give coordinates in a tuple as X and Z coordinate pair")
        return "Invalid Input, coordinates must be in a tuple"
    
    elif (thick_check(thickness)) == False:
        print("Wrong data type, thickness must be an integer or a float value")
        return "Invalid Input, thickness must be an integer or a float"

    elif len(lower_inner_coordinates) != 2 or len(mid_point_coordinates) != 2:
        print("The input tuples are too long, please check you have given a 2D coordinate for each points")
        return "Input tuples must be 2 element long - coordinate on XZ plane"


    else:
        lower_x, lower_z = lower_inner_coordinates
        mid_x, mid_z = mid_point_coordinates

        ### redifine values to be floats to make it look consistent 
        lower_x,lower_z, mid_x, mid_z, thickness = float(lower_x),float(lower_z), float(mid_x),float(mid_z), float(thickness)

        ### Define differences to avoid miss claculation due to signs
        base_length = mid_x - lower_x
        height = abs(mid_z - lower_z) * 2
        
        ### 10 points/tuples are returned from the initial 2 coordinates and thickness value
        p1 = (lower_x,lower_z)
        p2 = (p1[0]+base_length,p1[1])
        p3 = (p2[0],p2[1]+height)
        p4 = (p1[0],p1[1]+height)
        p5 = (p4[0],p4[1]+thickness)
        p6 = (p3[0],p4[1]+thickness)
        p7 = (p3[0]+thickness,p3[1])
        p8 = (p2[0]+thickness,p2[1])
        p9 = (p2[0],p2[1]-thickness)
        p10 = (lower_x,lower_z-thickness)

        ### Tuple holding the points that are being returned by the function
        points = (p1,p2,p3,p4,p5,p6,p7,p8,p9,p10)

        if test == True:
            print(points)

        return points

def tup_check(tup):
    check = type(tup) == tuple
    #print(check)
    return check

def thick_check(thickness):
    check = type(thickness) == float or type(thickness) == int
    #print(check)
    return check
    

