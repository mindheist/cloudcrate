import SwiftUI

@main
struct QuickQuizApp: App {
    @StateObject private var viewModel = QuizViewModel(questions: QuestionBank.defaultQuestions)

    var body: some Scene {
        WindowGroup {
            QuizView(viewModel: viewModel)
        }
    }
}
