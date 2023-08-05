#version 430

// nécéssaire pour que ça ne plante pas avec des cartes nvidia sur des petits échantillons
#pragma optionNV(unroll none)

// %%VARIABLE%% will be replaced with consts by python code
#define LAYOUT_SIZE %%LAYOUT_SIZE%%
#define NPART %%NPART%%
#define RCUT %%RCUT%%

#define LENGTH_X %%LENGTH_X%%
#define LENGTH_Y %%LENGTH_Y%%
#define SHIFT_X LENGTH_X/2// générique et logique
#define SHIFT_Y LENGTH_Y/2

#define X_PERIODIC %%X_PERIODIC%%
#define Y_PERIODIC %%Y_PERIODIC%%

layout (local_size_x=LAYOUT_SIZE, local_size_y=1, local_size_z=1) in;

layout (std430, binding=0) buffer in_0
{
    vec2 inpost[NPART];
};

layout (std430, binding=1) buffer in_1
{
    vec2 inposdt[NPART];
};


layout (std430, binding=2) buffer out_0
{
    mat2 outeps[NPART];
};



void main()
{
    const uint x = gl_GlobalInvocationID.x;

    mat2 X = mat2(0.0);
    mat2 Y = mat2(0.0);
    mat2 eps = mat2(0.0);

    if (x < NPART) { // On vérifie qu'on est bien associé à un atome
        const vec2 pos = inpost[x];
        vec2 posdt = inposdt[x];
        for (uint n = 0; n<NPART; n++){
            if (n!=x) {
                vec2 cpos = vec2(inpost[n]);
                vec2 distxy = pos - cpos;

                vec2 cposdt = vec2(inposdt[n]);
                // Conditions périodiques de bord
                /* On trouvera des tutos sur le net qui disent de vectoriser les tests suivants à la main
                 * mais le compilateur est malin et le fait tout seul.
                 */
                #if X_PERIODIC
                if (distxy.x<(-SHIFT_X)) {
                    distxy.x+=LENGTH_X;
                }
                if (distxy.x>SHIFT_X) {
                    distxy.x-=LENGTH_X;
                }
                #endif

                #if Y_PERIODIC
                if (distxy.y<(-SHIFT_Y)) {
                    distxy.y+=LENGTH_Y;
                }
                if (distxy.y>SHIFT_Y) {
                    distxy.y-=LENGTH_Y;
                }
                #endif


                /* Ce test accélère d'environ 15%, puisqu'on saute les étapes de multipication+somme du calcul de distance
                 * pour voir si on est dans la sphère
                 */
                if (abs(distxy.x)<RCUT && abs(distxy.y)<RCUT) {
                    float dist = length(distxy);
                    if (dist<RCUT) {
                        vec2 distxydt = posdt - cposdt;
                        #if X_PERIODIC
                            if (distxydt.x<(-SHIFT_X)) {
                                distxydt.x+=LENGTH_X;
                            }
                            if (distxydt.x>SHIFT_X) {
                                distxydt.x-=LENGTH_X;
                            }
                        #endif

                        #if Y_PERIODIC
                            if (distxydt.y<(-SHIFT_Y)) {
                                distxydt.y+=LENGTH_Y;
                            }
                            if (distxydt.y>SHIFT_Y) {
                                distxydt.y-=LENGTH_Y;
                            }
                        #endif
                        for (uint i = 0; i<2; i++){
                            for (uint j = 0; j<2; j++){
                                X[i][j] += distxy[i]*distxydt[j];
                                Y[i][j] += distxydt[i]*distxydt[j];
                            }
                        }
                    }
                }
            }
        }
        eps = X*inverse(Y) - mat2(1.0);
        outeps[x] = eps;
    }
}