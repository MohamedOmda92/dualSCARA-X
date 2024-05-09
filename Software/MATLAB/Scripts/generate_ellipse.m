function wpts = generate_ellipse(center,xAmp,yAmp,options)
%{
GENERATE_ellipse Creates ellipse waypoints.
These waypoints could be used later for trajectory generation

@param: center (1x2 double) -> Circle center XY coordinates.
@param: xAmp (1x1 double) -> X axes length of non-rotated ellipse.
@param: yAmp (1x1 double) -> Y axes length of non-rotated ellipse.

@option: Start -> Start angle of path following.
@option: Angle -> Angle of rotation of the ellipse ccw from +ve x-axis.
@option: Direction -> Direction of path following from `Start`.

`Start` valid values shoud be >= 0
`Direction` valid values are: {'cw', 'ccw'}

@return: wpts (2xN double) -> Array represent XY coordinates of ...
    ... circle N points + start point agian for closed loop.
%}

arguments
    center (1,2) double {mustBeNumeric, mustBeNonNan}
    xAmp (1,1) double {mustBeNumeric, mustBePositive}
    yAmp (1,1) double {mustBeNumeric, mustBePositive}
    options.Start (1,1) double {mustBeNumeric, mustBeNonnegative} = 0
    options.Angle (1,1) double {mustBeNumeric, mustBeNonNan}
    options.Direction {mustBeMember(options.Direction, ["cw","ccw"])} = "ccw"
end

% Valid values of `Angle` parameters
start = options.Start;
rotationAngle = options.Angle;
dir = options.Direction;
directions = ["cw","ccw"];
step = pi/180;

if strcmp(dir, directions(1))
    % cw
    t = [start:-step:0, 2*pi:-step:start];
elseif strcmp(dir, directions(2))
    % ccw
    t = [start:step:2*pi, 0:step:start];
end

transformMatrix = [
    cos(rotationAngle), sin(rotationAngle);
    -sin(rotationAngle), cos(rotationAngle)];

xAligned = xAmp * cos(t) + center(1);
yAligned = yAmp * sin(t) + center(2);

xyAligned = [xAligned; yAligned]';
xyRotated = xyAligned * transformMatrix;

xRotated = xyRotated(:, 1)';
yRotated = xyRotated(:, 2)';

wpts = [xRotated; yRotated];

end