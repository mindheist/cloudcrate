import Foundation

struct Question: Identifiable, Equatable {
    struct Option: Identifiable, Equatable {
        let id: UUID
        let text: String

        init(id: UUID = UUID(), text: String) {
            self.id = id
            self.text = text.trimmingCharacters(in: .whitespacesAndNewlines)
        }
    }

    let id: UUID
    let prompt: String
    let options: [Option]
    let correctOptionID: Option.ID
    let explanation: String?

    init(
        id: UUID = UUID(),
        prompt: String,
        options: [Option],
        correctOptionID: Option.ID,
        explanation: String? = nil
    ) {
        precondition(!options.isEmpty, "Questions must offer at least one option")
        precondition(options.contains(where: { $0.id == correctOptionID }), "Correct option must exist in options list")

        self.id = id
        self.prompt = prompt.trimmingCharacters(in: .whitespacesAndNewlines)
        self.options = options
        self.correctOptionID = correctOptionID
        self.explanation = explanation?.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    init(prompt: String, answers: [String], correctIndex: Int, explanation: String? = nil) {
        precondition(!answers.isEmpty, "Questions must offer at least one option")
        precondition(answers.indices.contains(correctIndex), "Correct answer index is out of bounds")

        let builtOptions = answers.map { Option(text: $0) }
        let correctID = builtOptions[correctIndex].id
        self.init(
            prompt: prompt,
            options: builtOptions,
            correctOptionID: correctID,
            explanation: explanation
        )
    }
}
