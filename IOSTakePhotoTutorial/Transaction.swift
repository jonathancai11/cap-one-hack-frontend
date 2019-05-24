//
//  Transaction.swift
//  IOSTakePhotoTutorial
//
//  Created by Jonathan Cai on 5/23/19.
//  Copyright © 2019 Arthur Knopper. All rights reserved.
//

import Foundation

struct Transaction: Codable{
    var vendor: String
    var time: String
    var date: String
    var items: [[String: AnyObject]]
    var total: Double
    
}
struct TransactionDataResponse: Codable {
    var success : Bool
    var data : [Transaction]
}
