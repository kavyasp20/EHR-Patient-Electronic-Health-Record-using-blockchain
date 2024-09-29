// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 <= 0.9;

contract EHR {
    string public users;
    string public report;
    string public appointments;
   

    function addUsers(string memory u) public {
        users = u;	
    }

    function getUsers() public view returns (string memory) {
        return users;
    }


    function addreport(string memory ca) public {
        report = ca;
    }

    function getreport() public view returns (string memory) {
        return report;
    }

    function addappointments(string memory p) public {
        appointments = p;
    }

    function getappointments() public view returns (string memory) {
        return appointments;
    }

   

    constructor() public {
    users = "";
    report = "";
    appointments = "";
    
    }
}