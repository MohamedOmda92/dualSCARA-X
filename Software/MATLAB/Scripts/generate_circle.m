function wpts = generate_circle(r,center,options)
%{
GENERATE_CIRCLE Creates circle waypoints.
These waypoints could be used later for trajectory generation

@param: r (1x1 double) -> Circle radius.
@param: center (1x2 double) -> Circle center XY coordinates.

@option: Start -> Start angle of path following.
@option: Direction -> Direction of path following from `Start`.

`Start` valid values shoud be >= 0
`Direction` valid values are: {'cw', 'ccw'}

@return: wpts (2xN double) -> Array represent XY coordinates of ...
    ... circle N points + start point agian for closed loop.
%}

arguments
    r (1,1) double {mustBeNumeric, mustBeNonNan, mustBePositive}
    center (1,2) double {mustBeNumeric, mustBeNonNan}
    options.Start {mustBeNumeric, mustBeNonNan, mustBeNonnegative} = 0
    options.Direction {mustBeMember(options.Direction, ["cw","ccw"])} = "ccw"
end

% Valid values of `Start` and `Direction` parameters
start = options.Start;
dir = options.Direction;
directions = ["cw","ccw"];

x = center(1);
y = center(2);
chord = 0.001; % 1 mm constant

theta = 2*asin(chord/(2*r)); % Chord = 2*radius*sin(theta/2)

if strcmp(dir, directions(1))
    % cw
    th = [start:-theta:0, 2*pi:-theta:start];

elseif strcmp(dir, directions(2))
    %  ccw
    th = [start:theta:2*pi, 0:theta:start];
end

xunit = r * cos(th) + x;
yunit = r * sin(th) + y;

wpts = [xunit; yunit];

end