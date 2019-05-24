//
//  NetworkManager.swift
//  IOSTakePhotoTutorial
//
//  Created by Jonathan Cai on 5/23/19.
//  Copyright © 2019 Arthur Knopper. All rights reserved.
//

import Foundation
import Alamofire

class NetworkManager {
    
    private static let baseURL = "http://0.0.0.0"
    
    //static func getTransactions()
    
    static func getTransactions(completion: @escaping ([Transaction]) -> Void){
        let url = "\(baseURL)/api/user/"
        Alamofire.request(url, method: .get, parameters: [:], encoding: Alamofire.JSONEncoding.default, headers: [:]).validate().responseData(){
            response in
            switch response.result {
            case .success(let data):
                let jsonDecoder = JSONDecoder()
                if let transactionRes = try? jsonDecoder.decode(TransactionDataResponse.self, from: data) {
                    let transactions = transactionRes.data
                    completion(transactions)
                }
                else {
                    print("Invalid response data")
                }
            case .failure( _):
                print("failed to connect to backend")
            }
        }
    }
    
    
//    static func get_request(path : String) -> [String: Any] {
//
//        let url = "http://0.0.0.0:8080/" + path
//        let req_url = URL(string: url)!
//        var request = URLRequest(url: req_url)
//        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
//        request.setValue("close", forHTTPHeaderField: "Connection")
//        request.httpMethod = "GET"
//        let parameters: [String: Any] = [:]
//        do {
//            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted)
//            // pass dictionary to data object and set it as request body
//        } catch let error {
//            print(error.localizedDescription)
//            print("Error setting http body")
//        }
//
//        var responseData : Data? = nil
//
//        let task = URLSession.shared.dataTask(with: request) { data, response, error in
//            guard let data = data,
//                let response = response as? HTTPURLResponse,
//                error == nil else {                                              // check for fundamental networking error
//                    print("error", error ?? "Unknown error")
//                    return
//            }
//
//            print("Received response from server")
//
//            guard (200 ... 299) ~= response.statusCode else {                    // check for http errors
//                print("statusCode should be 2xx, but is \(response.statusCode)")
//                return
//            }
//            responseData = data
//        }
//        print("Sending request")
//        task.resume()
//
//        while (responseData == nil) {
//            //                print("Waiting")
//        }
//        //            return (responseString)
//        do {
//            return try JSONSerialization.jsonObject(with: responseData!, options: []) as! [String: Any]
//        } catch {
//            print("error occurred")
//        }
//        return ["error": true]
//    }

}
