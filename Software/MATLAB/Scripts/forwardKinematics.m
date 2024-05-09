function [x, y] = forwardKinematics(q1, q2)
la = 0.100;
lb = 0.220;
lc = 0.230;

E = 2*lb*(lc + (la*(cos(q2) - cos(q1))));
F = (2*la*lb*sin(q2)) - (2*la*lb*sin(q1));
G = (lc^2) + (2*(la^2)) + (2*lc*la*cos(q2)) - (2*lc*la*cos(q1)) - (2*(la^2)*cos(q2 - q1));

% display(theta2 * 180 / 3.1415);

theta2 = 2*atan((-F - sqrt( (E^2) + (F^2) - (G^2) )) / (G - E));

x = lc + (la*cos(q2)) + (lb*cos(theta2));
y = (la*sin(q2)) + (lb*sin(theta2));

x = x - 0.115;