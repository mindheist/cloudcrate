import SwiftUI

struct QuizView: View {
    @ObservedObject var viewModel: QuizViewModel

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 24) {
                header
                questionCard
                optionsList
                explanationSection
                Spacer()
                actionButtons
            }
            .padding(24)
            .background(
                LinearGradient(
                    colors: [Color(.systemBackground), Color(.secondarySystemBackground)],
                    startPoint: .top,
                    endPoint: .bottom
                )
                .ignoresSafeArea()
            )
            .navigationTitle("Quick Quiz")
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(viewModel.progressText)
                .font(.headline)
                .foregroundStyle(.secondary)
            ProgressView(value: Double(viewModel.currentIndex + 1), total: Double(viewModel.questions.count))
            Text(viewModel.scoreText)
                .font(.subheadline)
                .bold()
        }
    }

    private var questionCard: some View {
        Text(viewModel.currentQuestion.prompt)
            .font(.title2.weight(.semibold))
            .padding()
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(RoundedRectangle(cornerRadius: 16).fill(Color(.tertiarySystemBackground)))
    }

    private var optionsList: some View {
        VStack(spacing: 12) {
            ForEach(viewModel.currentQuestion.options) { option in
                OptionButton(
                    option: option,
                    isSelected: option.id == viewModel.selectedOptionID,
                    isCorrect: option.id == viewModel.currentQuestion.correctOptionID,
                    hasAnswered: viewModel.hasAnswered
                ) {
                    viewModel.select(option: option)
                }
                .disabled(viewModel.hasAnswered)
            }
        }
    }

    private var explanationSection: some View {
        Group {
            if viewModel.hasAnswered, let explanation = viewModel.currentQuestion.explanation {
                Text(explanation)
                    .font(.callout)
                    .foregroundStyle(.secondary)
                    .padding(.horizontal)
            }
        }
    }

    private var actionButtons: some View {
        VStack(spacing: 12) {
            if viewModel.isComplete {
                Button(action: { viewModel.restart() }) {
                    Label("Restart Quiz", systemImage: "arrow.clockwise")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
            } else {
                Button(action: viewModel.goToNextQuestion) {
                    Label("Next", systemImage: "chevron.right")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .disabled(!viewModel.hasAnswered)
            }

            Button(action: { viewModel.restart(shuffleQuestions: false) }) {
                Label("Start Over (same order)", systemImage: "arrow.counterclockwise")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
        }
    }
}

private struct OptionButton: View {
    let option: Question.Option
    let isSelected: Bool
    let isCorrect: Bool
    let hasAnswered: Bool
    let tapAction: () -> Void

    var body: some View {
        Button(action: tapAction) {
            HStack {
                Text(option.text)
                    .font(.body.weight(.medium))
                    .multilineTextAlignment(.leading)
                Spacer()
                if hasAnswered {
                    Image(systemName: isCorrect ? "checkmark.circle.fill" : (isSelected ? "xmark.circle.fill" : "circle"))
                        .foregroundStyle(iconColor)
                }
            }
            .padding()
            .frame(maxWidth: .infinity)
        }
        .buttonStyle(.plain)
        .background(RoundedRectangle(cornerRadius: 14).fill(backgroundColor))
        .overlay(
            RoundedRectangle(cornerRadius: 14)
                .stroke(borderColor, lineWidth: 1)
        )
    }

    private var backgroundColor: Color {
        guard hasAnswered else {
            return Color(.secondarySystemBackground)
        }
        if isCorrect {
            return Color.green.opacity(0.2)
        }
        if isSelected {
            return Color.red.opacity(0.2)
        }
        return Color(.secondarySystemBackground)
    }

    private var borderColor: Color {
        guard hasAnswered else {
            return Color.clear
        }
        return isCorrect ? .green : (isSelected ? .red : .clear)
    }

    private var iconColor: Color {
        isCorrect ? .green : (isSelected ? .red : .secondary)
    }
}

#Preview
struct QuizView_Previews: PreviewProvider {
    static var previews: some View {
        QuizView(viewModel: QuizViewModel(questions: QuestionBank.defaultQuestions))
    }
}
