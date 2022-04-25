// Prelab for lab 2 EECE2160
#include <iostream>


// global variables for array
int *v;
int size;

int count;

void Initialize(){
    // give count and size basic values
    count = 0;
    size = 2;
    // free up space for array of size 2 and point v to it
    int *arr = new int[size];
    v = arr;
}

void Finalize(){
    // free up memory
    delete [] v;
}

void Menu(){
    // give user main menu (put in function to declutter main)
    std::cout<<"\n";
    std::cout<<"\n";
    std::cout<<"Main Menu \n";
    std::cout<<"1. Print the Array\n";
    std::cout<<"2. Append element at the end\n";
    std::cout<<"3. Remove last element \n";
    std::cout<<"4. Insert one element \n";
    std::cout<<"5. Exit \n";
    std::cout<<"Select an option: \n";
}

void Grow(){
    // make new pointer for array thats double the size
    std::cout<<"Vector Grown \n";
    std::cout<<"Previous Capacity: "<<size<<" \n";
    size = size* 2;
    std::cout<<"New Capacity: "<<size<<" \n";

    int *nv = new int[size];
    // put elements of v in nv
    for(int i = 0; i < size; i++){
        nv[i] = v[i];
    }
    // make v = nv
    delete [] v;
    v = nv;
}

void AddElement(){
    // grow array if necessary
    if(count == size){
        Grow();
    }
    // get new element
    int new_el;
    std::cout<<"Enter the new element \n";
    std::cin>>new_el;
    // put it in the array
    v[count + 1] = new_el;
    count++;
}

void PrintVector(){
    // iterate over array and cout each element
   
    for(int *i =v; i < v + count; i++){
        std::cout<<*i<<" ";
    }
    std::cout<<"\n";
   
}
int main() {
    // do after memory is covered in class
    Initialize();
    int option;

    // switch cases for menu option
    bool go = true;
    while(go == true) {
        Menu();
        // give user main menu
        std::cin>>option;
        switch (option) {
            case 1 :
                std::cout << "You selected Print the Array\n";
                PrintVector();
                break;
            case 2 :
                std::cout << "You selected Append element at the end \n";
                AddElement();
                break;
            case 3 :
                std::cout << "You selected Remove last element \n";
                break;
            case 4 :
                std::cout << "You selected Insert one element \n";
                break;
            case 5 :
                std::cout << "You selected Exit \n";
                go = false;
                break;
            default :
                std::cout << "Enter a valid option: \n";
                std::cin >> option;

        }
        // exit while loop
        if(go == false) break;
    }

   
    Finalize();
    return 0;
}