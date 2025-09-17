//
//  CrisisResponseSDK.swift
//  CrisisResponseSDK
//
//  Created by GemmaSOS Team
//  Copyright © 2024 GemmaSOS. All rights reserved.
//

import Foundation
import UIKit

// MARK: - Crisis Types
public enum CrisisType: String, CaseIterable {
    case selfHarm = "self_harm"
    case suicide = "suicide"
    case violence = "violence"
    case abuse = "abuse"
    case overdose = "overdose"
    case none = "none"
    
    public var displayName: String {
        switch self {
        case .selfHarm: return "Self-Harm"
        case .suicide: return "Suicide Risk"
        case .violence: return "Violence"
        case .abuse: return "Abuse"
        case .overdose: return "Overdose"
        case .none: return "No Crisis"
        }
    }
}

// MARK: - Risk Levels
public enum RiskLevel: String, CaseIterable {
    case immediate = "immediate"
    case high = "high"
    case medium = "medium"
    case low = "low"
    case none = "none"
    
    public var displayName: String {
        switch self {
        case .immediate: return "Immediate Risk"
        case .high: return "High Risk"
        case .medium: return "Medium Risk"
        case .low: return "Low Risk"
        case .none: return "No Risk"
        }
    }
    
    public var color: UIColor {
        switch self {
        case .immediate: return .systemRed
        case .high: return .systemOrange
        case .medium: return .systemYellow
        case .low: return .systemBlue
        case .none: return .systemGreen
        }
    }
}

// MARK: - Crisis Resource
public struct CrisisResource {
    public let name: String
    public let number: String?
    public let website: String?
    public let description: String?
    
    public init(name: String, number: String? = nil, website: String? = nil, description: String? = nil) {
        self.name = name
        self.number = number
        self.website = website
        self.description = description
    }
}

// MARK: - Safety Plan
public struct SafetyPlan {
    public let immediateActions: [String]
    public let copingStrategies: [String]
    public let warningSigns: [String]
    public let emergencyContacts: [String]
    
    public init(immediateActions: [String], copingStrategies: [String], warningSigns: [String], emergencyContacts: [String]) {
        self.immediateActions = immediateActions
        self.copingStrategies = copingStrategies
        self.warningSigns = warningSigns
        self.emergencyContacts = emergencyContacts
    }
}

// MARK: - Crisis Analysis Result
public struct CrisisAnalysisResult {
    public let isCrisis: Bool
    public let crisisType: CrisisType
    public let confidence: Float
    public let riskLevel: RiskLevel
    public let response: String
    public let resources: [CrisisResource]
    public let safetyPlan: SafetyPlan?
    public let immediateRisk: Bool
    public let timestamp: Date
    
    public init(isCrisis: Bool, crisisType: CrisisType, confidence: Float, riskLevel: RiskLevel, response: String, resources: [CrisisResource], safetyPlan: SafetyPlan? = nil, immediateRisk: Bool = false) {
        self.isCrisis = isCrisis
        self.crisisType = crisisType
        self.confidence = confidence
        self.riskLevel = riskLevel
        self.response = response
        self.resources = resources
        self.safetyPlan = safetyPlan
        self.immediateRisk = immediateRisk
        self.timestamp = Date()
    }
}

// MARK: - Crisis Response SDK
public class CrisisResponseSDK {
    
    // MARK: - Properties
    private let crisisDetector: CrisisDetector
    private let responseGenerator: ResponseGenerator
    private let safetySystem: SafetySystem
    
    // MARK: - Initialization
    public init() {
        self.crisisDetector = CrisisDetector()
        self.responseGenerator = ResponseGenerator()
        self.safetySystem = SafetySystem()
    }
    
    // MARK: - Public Methods
    
    /// Analyze text for crisis indicators
    /// - Parameter text: Text to analyze
    /// - Returns: Crisis analysis result
    public func analyzeText(_ text: String) -> CrisisAnalysisResult {
        // Validate input
        let validation = safetySystem.validateInput(text: text)
        guard validation.isSafe else {
            return CrisisAnalysisResult(
                isCrisis: false,
                crisisType: .none,
                confidence: 0.0,
                riskLevel: .none,
                response: "Content cannot be processed safely. Please rephrase your message.",
                resources: []
            )
        }
        
        // Detect crisis
        let detection = crisisDetector.detectCrisis(from: text)
        
        if detection.isCrisisDetected {
            // Generate crisis response
            let response = responseGenerator.generateResponse(
                for: detection.crisisType,
                userMessage: text,
                confidence: detection.confidence,
                immediateRisk: detection.immediateRisk
            )
            
            return CrisisAnalysisResult(
                isCrisis: true,
                crisisType: detection.crisisType,
                confidence: detection.confidence,
                riskLevel: detection.riskLevel,
                response: response.text,
                resources: response.resources,
                safetyPlan: response.safetyPlan,
                immediateRisk: detection.immediateRisk
            )
        } else {
            return CrisisAnalysisResult(
                isCrisis: false,
                crisisType: .none,
                confidence: detection.confidence,
                riskLevel: .none,
                response: "No crisis indicators detected. I'm here to listen and support you.",
                resources: []
            )
        }
    }
    
    /// Analyze image for crisis indicators
    /// - Parameter image: Image to analyze
    /// - Returns: Crisis analysis result
    public func analyzeImage(_ image: UIImage) -> CrisisAnalysisResult {
        // Convert UIImage to data for processing
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            return CrisisAnalysisResult(
                isCrisis: false,
                crisisType: .none,
                confidence: 0.0,
                riskLevel: .none,
                response: "Could not process image. Please try again.",
                resources: []
            )
        }
        
        // Validate input
        let validation = safetySystem.validateInput(imageData: imageData)
        guard validation.isSafe else {
            return CrisisAnalysisResult(
                isCrisis: false,
                crisisType: .none,
                confidence: 0.0,
                riskLevel: .none,
                response: "Image cannot be processed safely.",
                resources: []
            )
        }
        
        // Detect crisis
        let detection = crisisDetector.detectCrisis(from: imageData)
        
        if detection.isCrisisDetected {
            // Generate crisis response
            let response = responseGenerator.generateResponse(
                for: detection.crisisType,
                userMessage: "Image analysis",
                confidence: detection.confidence,
                immediateRisk: detection.immediateRisk
            )
            
            return CrisisAnalysisResult(
                isCrisis: true,
                crisisType: detection.crisisType,
                confidence: detection.confidence,
                riskLevel: detection.riskLevel,
                response: response.text,
                resources: response.resources,
                safetyPlan: response.safetyPlan,
                immediateRisk: detection.immediateRisk
            )
        } else {
            return CrisisAnalysisResult(
                isCrisis: false,
                crisisType: .none,
                confidence: detection.confidence,
                riskLevel: .none,
                response: "No crisis indicators detected in image.",
                resources: []
            )
        }
    }
    
    /// Get crisis resources for a specific type
    /// - Parameter crisisType: Type of crisis
    /// - Returns: Array of crisis resources
    public func getResources(for crisisType: CrisisType) -> [CrisisResource] {
        return responseGenerator.getResources(for: crisisType)
    }
    
    /// Get general crisis resources
    /// - Returns: Array of general crisis resources
    public func getGeneralResources() -> [CrisisResource] {
        return responseGenerator.getGeneralResources()
    }
    
    /// Check if content is safe to process
    /// - Parameter text: Text to validate
    /// - Returns: Validation result
    public func validateContent(_ text: String) -> (isSafe: Bool, warnings: [String], recommendations: [String]) {
        let validation = safetySystem.validateInput(text: text)
        return (validation.isSafe, validation.warnings, validation.recommendations)
    }
    
    /// Get privacy information
    /// - Returns: Privacy information dictionary
    public func getPrivacyInfo() -> [String: Any] {
        return safetySystem.getPrivacySummary()
    }
}

// MARK: - Internal Classes (Mock implementations for demo)
private class CrisisDetector {
    func detectCrisis(from text: String) -> CrisisDetectionResult {
        // Mock implementation - in real app, this would use the actual Python model
        let crisisKeywords = [
            "hurt myself", "cut", "suicide", "kill myself", "end it all",
            "violence", "attack", "abuse", "hit me", "overdose"
        ]
        
        let textLower = text.lowercased()
        let hasCrisisKeywords = crisisKeywords.contains { textLower.contains($0) }
        
        if hasCrisisKeywords {
            let crisisType = determineCrisisType(from: textLower)
            let confidence = Float.random(in: 0.6...0.9)
            let immediateRisk = textLower.contains("tonight") || textLower.contains("now") || textLower.contains("today")
            
            return CrisisDetectionResult(
                isCrisisDetected: true,
                crisisType: crisisType,
                confidence: confidence,
                riskLevel: immediateRisk ? .immediate : .high,
                immediateRisk: immediateRisk
            )
        } else {
            return CrisisDetectionResult(
                isCrisisDetected: false,
                crisisType: .none,
                confidence: Float.random(in: 0.1...0.3),
                riskLevel: .none,
                immediateRisk: false
            )
        }
    }
    
    func detectCrisis(from imageData: Data) -> CrisisDetectionResult {
        // Mock implementation for image analysis
        return CrisisDetectionResult(
            isCrisisDetected: false,
            crisisType: .none,
            confidence: 0.1,
            riskLevel: .none,
            immediateRisk: false
        )
    }
    
    private func determineCrisisType(from text: String) -> CrisisType {
        if text.contains("hurt myself") || text.contains("cut") {
            return .selfHarm
        } else if text.contains("suicide") || text.contains("kill myself") || text.contains("end it all") {
            return .suicide
        } else if text.contains("violence") || text.contains("attack") {
            return .violence
        } else if text.contains("abuse") || text.contains("hit me") {
            return .abuse
        } else if text.contains("overdose") {
            return .overdose
        } else {
            return .none
        }
    }
}

private class ResponseGenerator {
    func generateResponse(for crisisType: CrisisType, userMessage: String, confidence: Float, immediateRisk: Bool) -> CrisisResponse {
        let responseText = generateResponseText(for: crisisType, immediateRisk: immediateRisk)
        let resources = getResources(for: crisisType)
        let safetyPlan = immediateRisk ? generateSafetyPlan() : nil
        
        return CrisisResponse(
            text: responseText,
            resources: resources,
            safetyPlan: safetyPlan
        )
    }
    
    func getResources(for crisisType: CrisisType) -> [CrisisResource] {
        switch crisisType {
        case .selfHarm:
            return [
                CrisisResource(name: "Self-Injury Outreach & Support", website: "sioutreach.org"),
                CrisisResource(name: "To Write Love on Her Arms", website: "twloha.com")
            ]
        case .suicide:
            return [
                CrisisResource(name: "National Suicide Prevention Lifeline", number: "988"),
                CrisisResource(name: "Crisis Text Line", text: "Text HOME to 741741")
            ]
        case .violence:
            return [
                CrisisResource(name: "National Domestic Violence Hotline", number: "1-800-799-7233"),
                CrisisResource(name: "National Sexual Assault Hotline", number: "1-800-656-4673")
            ]
        case .abuse:
            return [
                CrisisResource(name: "National Domestic Violence Hotline", number: "1-800-799-7233"),
                CrisisResource(name: "Childhelp National Child Abuse Hotline", number: "1-800-4-A-CHILD")
            ]
        case .overdose:
            return [
                CrisisResource(name: "SAMHSA National Helpline", number: "1-800-662-4357"),
                CrisisResource(name: "National Poison Control Center", number: "1-800-222-1222")
            ]
        case .none:
            return []
        }
    }
    
    func getGeneralResources() -> [CrisisResource] {
        return [
            CrisisResource(name: "National Suicide Prevention Lifeline", number: "988"),
            CrisisResource(name: "Crisis Text Line", text: "Text HOME to 741741"),
            CrisisResource(name: "Emergency Services", number: "911")
        ]
    }
    
    private func generateResponseText(for crisisType: CrisisType, immediateRisk: Bool) -> String {
        let baseResponses = [
            CrisisType.selfHarm: "I can hear that you're in a lot of pain right now. You don't have to go through this alone.",
            CrisisType.suicide: "I'm very concerned about you right now. Your life matters, and I want to help you stay safe.",
            CrisisType.violence: "I'm concerned about your safety. Violence is never the answer, and there are better ways to handle this.",
            CrisisType.abuse: "I'm so sorry this is happening to you. You don't deserve to be treated this way.",
            CrisisType.overdose: "I'm very concerned about your safety right now. If you've already taken something, please call emergency services immediately."
        ]
        
        let baseResponse = baseResponses[crisisType] ?? "I'm here to listen and support you."
        
        if immediateRisk {
            return "\(baseResponse) Please know that you don't have to face this alone. If you're in immediate danger, call 911 or 988 right now."
        } else {
            return "\(baseResponse) There are people who care about you and want to help you through this."
        }
    }
    
    private func generateSafetyPlan() -> SafetyPlan {
        return SafetyPlan(
            immediateActions: [
                "Call 911 or go to the nearest emergency room if you're in immediate danger",
                "Remove any means of self-harm from your immediate environment",
                "Stay with a trusted person or in a public place"
            ],
            copingStrategies: [
                "Practice deep breathing exercises",
                "Use grounding techniques (5-4-3-2-1 method)",
                "Reach out to a trusted friend or family member"
            ],
            warningSigns: [
                "Feeling hopeless or worthless",
                "Having thoughts of self-harm or suicide",
                "Feeling isolated or alone"
            ],
            emergencyContacts: [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "Emergency Services: 911"
            ]
        )
    }
}

private class SafetySystem {
    func validateInput(text: String) -> ValidationResult {
        // Mock validation - in real app, this would use the actual safety system
        let harmfulKeywords = ["detailed methods", "step by step", "how to"]
        let hasHarmfulContent = harmfulKeywords.contains { text.lowercased().contains($0) }
        
        return ValidationResult(
            isSafe: !hasHarmfulContent,
            warnings: hasHarmfulContent ? ["Potentially harmful content detected"] : [],
            recommendations: hasHarmfulContent ? ["Please rephrase your message"] : []
        )
    }
    
    func validateInput(imageData: Data) -> ValidationResult {
        // Mock validation for images
        return ValidationResult(isSafe: true, warnings: [], recommendations: [])
    }
    
    func getPrivacySummary() -> [String: Any] {
        return [
            "data_processing": "on_device_only",
            "data_storage": "temporary_metadata_only",
            "data_transmission": "none",
            "privacy_measures": [
                "No data sent to external servers",
                "All processing happens on device",
                "No permanent storage of user content"
            ]
        ]
    }
}

// MARK: - Supporting Types
private struct CrisisDetectionResult {
    let isCrisisDetected: Bool
    let crisisType: CrisisType
    let confidence: Float
    let riskLevel: RiskLevel
    let immediateRisk: Bool
}

private struct CrisisResponse {
    let text: String
    let resources: [CrisisResource]
    let safetyPlan: SafetyPlan?
}

private struct ValidationResult {
    let isSafe: Bool
    let warnings: [String]
    let recommendations: [String]
}
