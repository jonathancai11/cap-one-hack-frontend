//
//  ViewController.swift
//  IOSTakePhotoTutorial
//
//  Created by Arthur Knopper on 18/12/2018.
//  Copyright © 2018 Arthur Knopper. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UINavigationControllerDelegate, UIImagePickerControllerDelegate {
    var imagePicker: UIImagePickerController!

    @IBOutlet weak var imageView: UIImageView!
    @IBAction func takePhoto(_ sender: Any) {
        imagePicker =  UIImagePickerController()
        imagePicker.delegate = self
        imagePicker.sourceType = .camera
        
        present(imagePicker, animated: true, completion: nil)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print(get_request(path: "api/img"))
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        imagePicker.dismiss(animated: true, completion: nil)
        imageView.image = info[.originalImage] as? UIImage
    }
    
    func get_request(path : String) -> [String: Any] {
    
        let url = "http://0.0.0.0:8080/" + path
        let req_url = URL(string: url)!
        var request = URLRequest(url: req_url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("close", forHTTPHeaderField: "Connection")
        request.httpMethod = "GET"
        let parameters: [String: Any] = [:]
        do {
        request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted)
        // pass dictionary to data object and set it as request body
        } catch let error {
        print(error.localizedDescription)
        print("Error setting http body")
        }
    
        var responseData : Data? = nil
    
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
        guard let data = data,
        let response = response as? HTTPURLResponse,
        error == nil else {                                              // check for fundamental networking error
        print("error", error ?? "Unknown error")
        return
        }
    
        print("Received response from server")
    
        guard (200 ... 299) ~= response.statusCode else {                    // check for http errors
        print("statusCode should be 2xx, but is \(response.statusCode)")
        return
        }
        responseData = data
        }
        print("Sending request")
        task.resume()
    
        while (responseData == nil) {
        //                print("Waiting")
        }
        //            return (responseString)
        do {
        return try JSONSerialization.jsonObject(with: responseData!, options: []) as! [String: Any]
        } catch {
        print("error occurred")
        }
        return ["error": true]
        }


}

