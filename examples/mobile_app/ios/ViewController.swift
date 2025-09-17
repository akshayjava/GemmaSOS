//
//  ViewController.swift
//  CrisisResponseApp
//
//  Created by GemmaSOS Team
//  Copyright © 2024 GemmaSOS. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    // MARK: - IBOutlets
    @IBOutlet weak var textView: UITextView!
    @IBOutlet weak var analyzeButton: UIButton!
    @IBOutlet weak var resultLabel: UILabel!
    @IBOutlet weak var resourcesTableView: UITableView!
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var privacyButton: UIButton!
    
    // MARK: - Properties
    private let crisisSDK = CrisisResponseSDK()
    private var currentResult: CrisisAnalysisResult?
    private var resources: [CrisisResource] = []
    
    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupTableView()
    }
    
    // MARK: - Setup
    private func setupUI() {
        title = "Crisis Response App"
        
        // Configure text view
        textView.layer.borderColor = UIColor.systemGray4.cgColor
        textView.layer.borderWidth = 1.0
        textView.layer.cornerRadius = 8.0
        textView.font = UIFont.systemFont(ofSize: 16)
        textView.text = "Type your message here..."
        textView.textColor = UIColor.placeholderText
        
        // Configure analyze button
        analyzeButton.layer.cornerRadius = 8.0
        analyzeButton.backgroundColor = UIColor.systemBlue
        analyzeButton.setTitleColor(.white, for: .normal)
        
        // Configure result label
        resultLabel.numberOfLines = 0
        resultLabel.font = UIFont.systemFont(ofSize: 16)
        
        // Configure status label
        statusLabel.text = "Ready to analyze"
        statusLabel.textColor = UIColor.systemGreen
        
        // Configure privacy button
        privacyButton.setTitle("Privacy Info", for: .normal)
        privacyButton.setTitleColor(.systemBlue, for: .normal)
    }
    
    private func setupTableView() {
        resourcesTableView.delegate = self
        resourcesTableView.dataSource = self
        resourcesTableView.register(ResourceTableViewCell.self, forCellReuseIdentifier: "ResourceCell")
        resourcesTableView.isHidden = true
    }
    
    // MARK: - Actions
    @IBAction func analyzeButtonTapped(_ sender: UIButton) {
        guard let text = textView.text, !text.isEmpty, text != "Type your message here..." else {
            showAlert(title: "No Text", message: "Please enter some text to analyze.")
            return
        }
        
        // Show loading state
        analyzeButton.isEnabled = false
        analyzeButton.setTitle("Analyzing...", for: .normal)
        statusLabel.text = "Analyzing message..."
        statusLabel.textColor = UIColor.systemOrange
        
        // Perform analysis on background queue
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            guard let self = self else { return }
            
            let result = self.crisisSDK.analyzeText(text)
            
            DispatchQueue.main.async {
                self.handleAnalysisResult(result)
            }
        }
    }
    
    @IBAction func privacyButtonTapped(_ sender: UIButton) {
        let privacyInfo = crisisSDK.getPrivacyInfo()
        showPrivacyAlert(privacyInfo)
    }
    
    // MARK: - Analysis Handling
    private func handleAnalysisResult(_ result: CrisisAnalysisResult) {
        currentResult = result
        
        // Update UI based on result
        if result.isCrisis {
            handleCrisisDetected(result)
        } else {
            handleNoCrisisDetected(result)
        }
        
        // Reset button state
        analyzeButton.isEnabled = true
        analyzeButton.setTitle("Analyze Text", for: .normal)
    }
    
    private func handleCrisisDetected(_ result: CrisisAnalysisResult) {
        // Update status
        statusLabel.text = "Crisis detected - providing support"
        statusLabel.textColor = UIColor.systemRed
        
        // Update result label with crisis response
        resultLabel.text = result.response
        resultLabel.textColor = UIColor.systemRed
        
        // Show resources
        resources = result.resources
        resourcesTableView.reloadData()
        resourcesTableView.isHidden = false
        
        // Show crisis alert
        showCrisisAlert(result)
    }
    
    private func handleNoCrisisDetected(_ result: CrisisAnalysisResult) {
        // Update status
        statusLabel.text = "No crisis detected"
        statusLabel.textColor = UIColor.systemGreen
        
        // Update result label
        resultLabel.text = result.response
        resultLabel.textColor = UIColor.label
        
        // Hide resources
        resources = []
        resourcesTableView.isHidden = true
    }
    
    // MARK: - Alerts
    private func showCrisisAlert(_ result: CrisisAnalysisResult) {
        let alert = UIAlertController(
            title: "🚨 Crisis Support",
            message: "I've detected a crisis situation. I'm here to help and support you.",
            preferredStyle: .alert
        )
        
        // Add crisis-specific actions
        if result.immediateRisk {
            alert.addAction(UIAlertAction(title: "Call 911", style: .destructive) { _ in
                self.callEmergencyServices()
            })
            
            alert.addAction(UIAlertAction(title: "Call 988", style: .destructive) { _ in
                self.callCrisisHotline()
            })
        }
        
        // Add resource actions
        if !result.resources.isEmpty {
            alert.addAction(UIAlertAction(title: "View Resources", style: .default) { _ in
                self.showResourcesList(result.resources)
            })
        }
        
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        
        present(alert, animated: true)
    }
    
    private func showResourcesList(_ resources: [CrisisResource]) {
        let alert = UIAlertController(
            title: "Crisis Resources",
            message: "Here are resources that can help:",
            preferredStyle: .alert
        )
        
        for resource in resources {
            let actionTitle = resource.number != nil ? "\(resource.name) (\(resource.number!))" : resource.name
            alert.addAction(UIAlertAction(title: actionTitle, style: .default) { _ in
                if let number = resource.number {
                    self.callNumber(number)
                }
            })
        }
        
        alert.addAction(UIAlertAction(title: "Cancel", style: .cancel))
        
        present(alert, animated: true)
    }
    
    private func showPrivacyAlert(_ privacyInfo: [String: Any]) {
        let message = """
        Privacy Information:
        
        • All processing happens on your device
        • No data is sent to external servers
        • No permanent storage of your content
        • Complete privacy protection
        """
        
        let alert = UIAlertController(
            title: "🔒 Privacy Protection",
            message: message,
            preferredStyle: .alert
        )
        
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        
        present(alert, animated: true)
    }
    
    private func showAlert(title: String, message: String) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
    
    // MARK: - Actions
    private func callEmergencyServices() {
        if let url = URL(string: "tel:911") {
            UIApplication.shared.open(url)
        }
    }
    
    private func callCrisisHotline() {
        if let url = URL(string: "tel:988") {
            UIApplication.shared.open(url)
        }
    }
    
    private func callNumber(_ number: String) {
        let cleanNumber = number.replacingOccurrences(of: "[^0-9]", with: "", options: .regularExpression)
        if let url = URL(string: "tel:\(cleanNumber)") {
            UIApplication.shared.open(url)
        }
    }
}

// MARK: - UITableViewDataSource
extension ViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return resources.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ResourceCell", for: indexPath) as! ResourceTableViewCell
        let resource = resources[indexPath.row]
        cell.configure(with: resource)
        return cell
    }
}

// MARK: - UITableViewDelegate
extension ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        
        let resource = resources[indexPath.row]
        if let number = resource.number {
            callNumber(number)
        }
    }
}

// MARK: - UITextViewDelegate
extension ViewController: UITextViewDelegate {
    func textViewDidBeginEditing(_ textView: UITextView) {
        if textView.text == "Type your message here..." {
            textView.text = ""
            textView.textColor = UIColor.label
        }
    }
    
    func textViewDidEndEditing(_ textView: UITextView) {
        if textView.text.isEmpty {
            textView.text = "Type your message here..."
            textView.textColor = UIColor.placeholderText
        }
    }
}

// MARK: - ResourceTableViewCell
class ResourceTableViewCell: UITableViewCell {
    
    private let nameLabel = UILabel()
    private let detailLabel = UILabel()
    private let callButton = UIButton(type: .system)
    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        setupUI()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    private func setupUI() {
        // Configure name label
        nameLabel.font = UIFont.boldSystemFont(ofSize: 16)
        nameLabel.numberOfLines = 0
        nameLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(nameLabel)
        
        // Configure detail label
        detailLabel.font = UIFont.systemFont(ofSize: 14)
        detailLabel.textColor = UIColor.systemGray
        detailLabel.numberOfLines = 0
        detailLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(detailLabel)
        
        // Configure call button
        callButton.setTitle("Call", for: .normal)
        callButton.backgroundColor = UIColor.systemBlue
        callButton.setTitleColor(.white, for: .normal)
        callButton.layer.cornerRadius = 6
        callButton.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(callButton)
        
        // Set up constraints
        NSLayoutConstraint.activate([
            nameLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 8),
            nameLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
            nameLabel.trailingAnchor.constraint(equalTo: callButton.leadingAnchor, constant: -8),
            
            detailLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 4),
            detailLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
            detailLabel.trailingAnchor.constraint(equalTo: callButton.leadingAnchor, constant: -8),
            detailLabel.bottomAnchor.constraint(equalTo: contentView.bottomAnchor, constant: -8),
            
            callButton.centerYAnchor.constraint(equalTo: contentView.centerYAnchor),
            callButton.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -16),
            callButton.widthAnchor.constraint(equalToConstant: 60),
            callButton.heightAnchor.constraint(equalToConstant: 32)
        ])
    }
    
    func configure(with resource: CrisisResource) {
        nameLabel.text = resource.name
        
        if let number = resource.number {
            detailLabel.text = number
            callButton.isHidden = false
        } else if let website = resource.website {
            detailLabel.text = website
            callButton.isHidden = true
        } else {
            detailLabel.text = resource.description
            callButton.isHidden = true
        }
    }
}
