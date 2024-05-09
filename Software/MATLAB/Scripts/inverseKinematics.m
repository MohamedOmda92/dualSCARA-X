function [D1, D4] = inverseKinematics(Xp, Yp)
la = 0.100;
lb = 0.220;
lc = 0.230;

Xp = Xp + 0.115;

C = sqrt((Xp^2) + (Yp^2));
e = sqrt(((lc-Xp)^2) + (Yp^2));
D1 = atan(Yp/Xp) + acos((-(lb^2)+(la^2)+(C^2)) / (2*la*C));
D4 = 3.14 - atan((Yp)/(lc-Xp)) + acos((-(lb^2)+(la^2)+(e^2)) / (2*la*e));
