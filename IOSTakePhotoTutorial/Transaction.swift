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
    var items: [[String: String]]
    var total: Double
}

struct TransactionDataResponse: Codable {
    var transactions: [Transaction]
}

