// SPDX-License-Identifier: MIT
///* always put solidity version at the top of the script */
pragma solidity  ^0.6.0;

contract SimpleStorage {
    uint256 public favoriteNumber;

     /* 
     lecture notes
    bool favoriteBool = True;
    string favoriteString = "String";
    int256 favoriteInt = -5;
    address favoriteAddress = 0x743455077a8d9A651A0De75E4E4B31221ed045E9
    bytes32 favoriteBytes = "cat"
 */
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    //People public person = People({favoriteNumber:2, name:"Patrick"});

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
     //view pure no transaction; no state change then no transaction
    //pure functions do some time of math
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
}

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

//structs are ways to define new types in solidity
}