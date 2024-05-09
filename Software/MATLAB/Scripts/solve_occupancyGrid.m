function wpts = solve_occupancyGrid(occMap,start, goal, options)
    %{
    SOLVE_OCCUPANCYGRID Creates free-obstacles waypoints from start to goal pose.
    
    @param: occMap (NxP double) -> Grid of N rows and P columns with 0s or 1s.
    @param: start (1x2 double) -> Start pose with [Row Column] from lower-left.
    @param: start (1x2 double) -> End pose with [Row Column] from lower-left.
    
    @return: wpts (2xN double) -> Array of N waypoints used for path planning.
    %}
    
    arguments
        occMap (:,:) double {mustBeNumeric, mustBeNonNan}
        start (1,2) double {mustBeNumeric, mustBeNonNan, mustBePositive}
        goal (1,2) double {mustBeNumeric, mustBeNonNan, mustBePositive}
        options.Diagonal {mustBeMember(options.Diagonal, ["on","off"])} = "off"
    end
    
    % Properties Validation
    diagonalSearch = options.Diagonal;
    
    % Generate Binary Occupancy Grid
    map = binaryOccupancyMap(occMap);
    
    % Generation A* planner for given grid map
    planner = plannerAStarGrid(map, 'DiagonalSearch',diagonalSearch);
    
    % Generate waypoints of the shortest path between start and goal pose
    wpts = plan(planner,start,goal)';
    
    end