import matlab.engine
eng = matlab.engine.start_matlab()

wayPoints = matlab.double([[-0.02, 0.02, 0.02, -0.02, -0.02],
                           [0.15, 0.15, 0.25, 0.25, 0.151]])

numSamples = matlab.double([200])
EndTime = matlab.double([5])
eng.cd(r'Matlab')
eng.generate_trajectory(wayPoints, numSamples, EndTime)
eng.quit()