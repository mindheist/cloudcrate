import Foundation

enum QuestionBank {
    /// Replace the sample questions below with your own content.
    static let defaultQuestions: [Question] = [
        Question(
            prompt: "When did Apple introduce SwiftUI?",
            answers: ["2014", "2016", "2019", "2021"],
            correctIndex: 2,
            explanation: "SwiftUI debuted during WWDC19."
        ),
        Question(
            prompt: "Which keyword lets SwiftUI views refresh automatically when data changes?",
            answers: ["@Binding", "@State", "@Published", "@ObservedObject"],
            correctIndex: 1,
            explanation: "@State keeps local view state and triggers updates."
        ),
        Question(
            prompt: "What Xcode preview device most closely matches a standard iPhone size?",
            answers: ["iPhone SE", "iPhone 15 Pro", "Apple Watch Ultra", "iPad mini"],
            correctIndex: 1,
            explanation: "The 6.1\" class (e.g. iPhone 15 Pro) is the common default."
        )
    ]
}
