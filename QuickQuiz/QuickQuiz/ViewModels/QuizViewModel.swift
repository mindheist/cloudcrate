import Foundation
import SwiftUI

final class QuizViewModel: ObservableObject {
    @Published private(set) var questions: [Question]
    @Published private(set) var currentIndex: Int = 0
    @Published private(set) var score: Int = 0
    @Published private(set) var isComplete: Bool = false
    @Published var selectedOptionID: Question.Option.ID? = nil
    @Published private(set) var hasAnswered: Bool = false

    init(questions: [Question]) {
        precondition(!questions.isEmpty, "Provide at least one question")
        self.questions = questions
    }

    var currentQuestion: Question {
        questions[currentIndex]
    }

    var progressText: String {
        "Question \(currentIndex + 1) of \(questions.count)"
    }

    var scoreText: String {
        "Score: \(score) / \(questions.count)"
    }

    func select(option: Question.Option) {
        guard !hasAnswered else { return }
        selectedOptionID = option.id
        hasAnswered = true
        if option.id == currentQuestion.correctOptionID {
            score += 1
        }

        if currentIndex == questions.count - 1 {
            isComplete = true
        }
    }

    func goToNextQuestion() {
        guard currentIndex < questions.count - 1 else {
            isComplete = true
            return
        }

        currentIndex += 1
        selectedOptionID = nil
        hasAnswered = false
    }

    func restart(shuffleQuestions: Bool = true) {
        if shuffleQuestions {
            questions.shuffle()
        }

        currentIndex = 0
        score = 0
        isComplete = false
        selectedOptionID = nil
        hasAnswered = false
    }
}
