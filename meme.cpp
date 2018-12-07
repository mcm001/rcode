#include <iostream>
#include <math>
using namespace std;

int main() {
    float leg1;
    float leg2;
    float leg3;
    
    cout << "enter leg 1" << endl;
    cin >> leg1;
    cout << "enter leg 2" << endl;
    cin >> leg2;

    leg3 = sqrt( (leg1 * leg1) + (leg2 * leg2))
    cout << "the hypotinuse is ¨ << leg3 << endl;
}
