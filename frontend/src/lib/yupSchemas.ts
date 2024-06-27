// SPDX-FileCopyrightText: 2023 
//
// SPDX-License-Identifier: MPL-2.0

// skipcq: JS-C1003
import * as yup from 'yup';

export const ABCDQuestionSchema = yup
	.array()
	.of(
		yup.object({
			right: yup.boolean().required(),
			answer: yup.string().required('Você precisa de uma resposta')
		})
	)
	.min(2, 'Você precisa de pelo menos 2 respostas')
	.max(16, "Você não pode ter mais de 16 respostas");

export const VotingQuestionSchema = yup
	.array()
	.of(
		yup.object({
			answer: yup.string().required('Você precisa de uma resposta'),
			image: yup.string().optional().nullable()
		})
	)
	.min(2, 'Você precisa de pelo menos 2 respostas')
	.max(16, "Você não pode ter mais de 16 respostas");

export const RangeQuestionSchema = yup.object({
	min: yup.number(),
	max: yup.number(),
	min_correct: yup.number(),
	max_correct: yup.number()
});

export const TextQuestionSchema = yup
	.array()
	.of(
		yup.object({
			case_sensitive: yup.boolean().required(),
			answer: yup.string().required('Você precisa de uma resposta')
		})
	)
	.min(1, 'Você precisa de pelo menos uma resposta')
	.max(16, "Você não pode ter mais de 16 respostas");

export const dataSchema = yup.object({
	public: yup.boolean().required(),
	type: yup.string(),
	title: yup
		.string()
		.required('Título obrigatório'),
	description: yup
		.string()
		.required('Descrição obrigatória'),
	questions: yup
		.array()
		.of(
			yup.object({
				question: yup.string().required('Um título para a questão é obrigatório').max(299),
				time: yup.number().required().positive('Timer precisa ser positivo'),
				image: yup.string().nullable().lowercase(),
				answers: yup.lazy((v) => {
					if (Array.isArray(v)) {
						if (typeof v[0].right === 'boolean') {
							return ABCDQuestionSchema;
						} else if (typeof v[0].case_sensitive === 'boolean') {
							return TextQuestionSchema;
						} else if (v[0].id !== undefined) {
							return VotingQuestionSchema;
						} else if (v[0].answer !== undefined) {
							return VotingQuestionSchema;
						}
					} else if (typeof v === 'string' || v instanceof String) {
						return yup.string().required("The slide mustn't be empty").nullable();
					} else {
						return RangeQuestionSchema;
					}
				})
			})
		)
		.min(1, 'Você precisa de pelo menos 1 pergunta')
		.max(50, "Você não pode ter mais de 50 perguntas")
});
