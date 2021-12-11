clear
syms ax aa ab cx cy bx bY ax aY

E1 = ax==-32.1/1000*aa+32.14/1000*ab
E2 = -32/1000*aa+10.29*ab/1000==ax
E3 = 38.3/1000*aa+38.65/1000*ab==aY
E4 = 82*cy+21.86*cx+10.29*bx+38.66*bY==0.004*1000*ab
E5 = -200-32.19/1000*bx+38.3/1000*bY==0.003*aa
E6 = cx-bx==0.36*ax
E7 = cy-bY==0.36*aY
E8 = -cx-5000==4.6*ax
E9 = ab==-3.15*aa

S = solve(E1, E2, E3, E4, E5, E6, E7, E8, E9)

%eqns = [ax==-32.1/1000*ax+32.14/1000*ab,-32/1000*aa+10.29*ab/1000==ax, 38.3/1000*aa+38.65/1000*ab==aY,82*cy+21.86*cx+10.29*bx+38.66*bY==0.004*1000*ab, -200-32.19/1000*bx+38.3/1000*bY==0.003*aa,cx-bx==0.36*ax,cy-bY==0.36*aY, -cx-5000==4.6*ax,ab==-3.15*aa];
%answers = [ax aa ab cx cy bx bY ax aY]
%S = solve(eqns, answers)