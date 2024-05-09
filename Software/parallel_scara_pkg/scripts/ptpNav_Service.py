#! /usr/bin/env python
import rospy
from parallel_scara_pkg.srv import ptpNav

def ptpNav_response(request):
    
    print(f"Navigating to X: {request.x} \tY: {request.y}")



def main():
    rospy.init_node('ptpNav_service')

    rospy.Service('/ptp_nav', ptpNav, ptpNav_response)
    rospy.spin()



if __name__ == "__main__":

    try:
        main()

    except rospy.ROSInterruptException as e:
        print(e)