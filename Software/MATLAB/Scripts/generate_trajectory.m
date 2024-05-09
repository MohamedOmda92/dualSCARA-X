function M = generate_trajectory(wpts,time, timeStep, options)
%{
GENERATE_TRAJECTORY Creates velocity profile trajectory from waypoints.
This trajectory will be followed/tracked later through return distance,...
... velocity, acceleration(NOT USED) at each time interval.

At the the end of this function, all output variables are combined in ...
... an array that is:
1. Written to a CSV file
2. Returned by the function

@param: wpts (2xN double) -> Array of N waypoints used for path planning.
@param: time (1x1 double) -> Time taken to complete whole trajectory.

@return: M (7xN double) -> Array of combined time, dist, vel, acc. 
%}

arguments
    wpts (2,:) double {mustBeNumeric, mustBeNonNan}
    time (1,:) double {mustBeNumeric, mustBeNonNan}
    timeStep (1,1) double {mustBeNumeric, mustBeNonNan, mustBePositive} = 0.05
    options.timeMode {mustBeMember(options.timeMode, ["dist","abs","inc"])} = "dist"
end

% Properties Validation
timeMode = options.timeMode;
modes = ["dist","abs","inc"];

% Total trajecotry time provided (Distributed)
if strcmp(timeMode, modes(1))
    [~,n] = size(wpts);
    totalDist = 0;
    segments = [];

    for i = 1:n-1
        dist = norm(wpts(:,i) - wpts(:,i+1));
        segments = [segments dist];
        totalDist = totalDist + dist;   
    end
    
    durations = segments ./ totalDist .* time;

    t = [durations; durations]; % For trapveltraj()
    totalTime = time; % For samples no.


% Time for each waypoint provided (Absolute)
elseif strcmp(timeMode, modes(2))
    durations = [];
    for i = 1:length(time)-1
        dur = time(i+1) - time(i);
        durations = [durations dur];
        
        if durations(i) < 0
            error("One of waypoints time is miss provided. Make sure time is increasing.");
            break;
        end
    end
    
    t = [durations; durations]; % For trapveltraj()
    totalTime = sum(durations); % For samples no.


% Duration for each segment provided (Incremental)
elseif strcmp(timeMode, modes(3))
    t = [time; time]; % For trapveltraj()
    totalTime = sum(time); % For samples no.
end

% Calculate number of samples
samples = (totalTime / timeStep) + 1;

[q,qd,qdd,tsample] = trapveltraj(wpts, samples, "EndTime",t);

M = [tsample; q; qd; qdd];
headers = {'tsample','q1','q2','qd1','qd2','qdd1','qdd2'};
C = [headers; num2cell(M')];

writecell(C, 'trajectory.csv');
end