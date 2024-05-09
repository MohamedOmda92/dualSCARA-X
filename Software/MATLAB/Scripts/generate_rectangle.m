function wpts = generate_rectangle(h,w,pin,options)
%{
GENERATE_RECTANGLE Creates rectangle waypoints.
These waypoints could be used later for trajectory generation

@param: h (1x1 double) -> Height of rectangle (vertical side).
@param: w (1x1 double) -> Width of rectangle (horizontal side).
@param: pin (1x2 double) -> XY coordinates of a point at which ...
    ... the rectangle will be pinned.

@option: Anchor -> Location of anchor that will be aligned with `pin`
@option: Direction -> Direction of path following from `pin`

`Anchor` valid values are: {'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'}
`Direction` valid values are: {'cw', 'ccw'}

@return: wpts (2x5 double) -> Array represent XY coordinates of ...
    ... rectangle 4 corners + start point agian for closed loop.
%}

arguments

    h (1,1) double {mustBeNumeric, mustBeNonNan, mustBePositive}
    w (1,1) double {mustBeNumeric, mustBeNonNan, mustBePositive}
    pin (1,2) double {mustBeNumeric}
    options.Anchor {mustBeMember(options.Anchor, ["ne","nw","se","sw","n","s","e","w"])} = "sw"
    options.Direction {mustBeMember(options.Direction, ["cw","ccw"])} = "ccw"
end

% Half width and height for midpoint anchor operations
h2 = h / 2;
w2 = w / 2;

% Valid values of `Anchor` and `Direction` parameters
anchor = options.Anchor;
dir = options.Direction;
cornerAnchors = ["ne","nw","se","sw"];
midAnchors = ["n","s","e","w"];
directions = ["cw","ccw"];

% At case of corner anchors
if ismember(anchor, cornerAnchors)
    point1 = pin;
    point5 = [];
    if strcmp(anchor,cornerAnchors(1)) && strcmp(dir, directions(1))
       % ne cw
       point2 = [pin(1), pin(2)-h];
       point3 = [pin(1)-w, pin(2)-h];
       point4 = [pin(1)-w, pin(2)];
    elseif strcmp(anchor,cornerAnchors(1)) && strcmp(dir, directions(2))
        % ne ccw
        point2 = [pin(1)-w, pin(2)];
        point3 = [pin(1)-w, pin(2)-h];
        point4 = [pin(1), pin(2)-h];
    elseif strcmp(anchor,cornerAnchors(2)) && strcmp(dir, directions(1))
        % nw cw
        point2 = [pin(1)+w, pin(2)];
        point3 = [pin(1)+w, pin(2)-h];
        point4 = [pin(1), pin(2)-h];
    elseif strcmp(anchor,cornerAnchors(2)) && strcmp(dir, directions(2))
        % nw ccw
        point2 = [pin(1), pin(2)-h];
        point3 = [pin(1)+w, pin(2)-h];
        point4 = [pin(1)+w, pin(2)];
    elseif strcmp(anchor,cornerAnchors(3)) && strcmp(dir, directions(1))
        % se cw
        point2 = [pin(1)-w, pin(2)];
        point3 = [pin(1)-w, pin(2)+h];
        point4 = [pin(1), pin(2)+h];
    elseif strcmp(anchor,cornerAnchors(3)) && strcmp(dir, directions(2))
        % se ccw
        point2 = [pin(1), pin(2)+h];
        point3 = [pin(1)-w, pin(2)+h];
        point4 = [pin(1)-w, pin(2)];
    elseif strcmp(anchor,cornerAnchors(4)) && strcmp(dir, directions(1))
        % sw cw
        point2 = [pin(1), pin(2)+h];
        point3 = [pin(1)+w, pin(2)+h];
        point4 = [pin(1)+w, pin(2)];
    elseif strcmp(anchor,cornerAnchors(4)) && strcmp(dir, directions(2))
        % sw ccw
        point2 = [pin(1)+w, pin(2)];
        point3 = [pin(1)+w, pin(2)+h];
        point4 = [pin(1), pin(2)+h];
    end

% At case of mid-line anchors
elseif ismember(anchor, midAnchors)
    point1 = pin;
    if strcmp(anchor,midAnchors(1)) && strcmp(dir, directions(1))
        % n cw
        point2 = [pin(1)+w2 pin(2)];
        point3 = [pin(1)+w2 pin(2)-h];
        point4 = [pin(1)-w2 pin(2)-h];
        point5 = [pin(1)-w2 pin(2)];
    elseif strcmp(anchor,midAnchors(1)) && strcmp(dir, directions(2))
        % n ccw
        point2 = [pin(1)-w2 pin(2)];
        point3 = [pin(1)-w2 pin(2)-h];
        point4 = [pin(1)+w2 pin(2)-h];
        point5 = [pin(1)+w2 pin(2)];
    elseif strcmp(anchor,midAnchors(2)) && strcmp(dir, directions(1))
        % s cw
        point2 = [pin(1)-w2 pin(2)];
        point3 = [pin(1)-w2 pin(2)+h];
        point4 = [pin(1)+w2 pin(2)+h];
        point5 = [pin(1)+w2 pin(2)];
    elseif strcmp(anchor,midAnchors(2)) && strcmp(dir, directions(2))
        % s ccw
        point2 = [pin(1)+w2 pin(2)];
        point3 = [pin(1)+w2 pin(2)+h];
        point4 = [pin(1)-w2 pin(2)+h];
        point5 = [pin(1)-w2 pin(2)];
    elseif strcmp(anchor,midAnchors(3)) && strcmp(dir, directions(1))
        % e cw
        point2 = [pin(1) pin(2)-h2];
        point3 = [pin(1)-w pin(2)-h2];
        point4 = [pin(1)-w pin(2)+h2];
        point5 = [pin(1) pin(2)+h2];
    elseif strcmp(anchor,midAnchors(3)) && strcmp(dir, directions(2))
        % e ccw
        point2 = [pin(1) pin(2)+h2];
        point3 = [pin(1)-w pin(2)+h2];
        point4 = [pin(1)-w pin(2)-h2];
        point5 = [pin(1) pin(2)-h2];
    elseif strcmp(anchor,midAnchors(4)) && strcmp(dir, directions(1))
        % w cw
        point2 = [pin(1) pin(2)+h2];
        point3 = [pin(1)+w pin(2)+h2];
        point4 = [pin(1)+w pin(2)-h2];
        point5 = [pin(1) pin(2)-h2];
    elseif strcmp(anchor,midAnchors(4)) && strcmp(dir, directions(2))
        % w ccw
        point2 = [pin(1) pin(2)-h2];
        point3 = [pin(1)+w pin(2)-h2];
        point4 = [pin(1)+w pin(2)+h2];
        point5 = [pin(1) pin(2)+h2];
    end
end

if ~isempty(point5)
    wpts = [point1; point2; point3; point4; point5; point1]';

else
    wpts = [point1; point2; point3; point4; point1]';
end
end