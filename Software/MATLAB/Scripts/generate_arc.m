function wpts = generate_arc(r,center,thStart,thEnd)
%{
GENERATE_ARC Creates arc waypoints.
These waypoints could be used later for trajectory generation

@param: r (1x1 double) -> Arc radius.
@param: center (1x2 double) -> Circle center XY coordinates.
@param: thStart (1x1 double) -> Start angle of path following.
@param: thEnd (1x1 double) -> End angle of path following.

@return: wpts (2xN double) -> Array represent XY coordinates of ...
    ... arc N points.
%}

arguments
    r (1,1) double {mustBeNumeric, mustBeNonNan, mustBePositive}
    center (1,2) double {mustBeNumeric, mustBeNonNan, mustBeNonnegative}
    thStart (1,1) double {mustBeNumeric, mustBeNonNan, mustBeNonnegative}
    thEnd (1,1) double {mustBeNumeric, mustBeNonNan, mustBeNonnegative}
end

x = center(1);
y = center(2);
chord = 0.001; % 1 mm constant

theta = 2*asin(chord/(2*r)); % Chord = 2*radius*sin(theta/2)

if thStart < thEnd
    th = thStart:theta:thEnd;
    
elseif thStart > thEnd
    th = thStart:-theta:thEnd;
end

xunit = r * cos(th) + x;
yunit = r * sin(th) + y;

wpts = [xunit; yunit];

end