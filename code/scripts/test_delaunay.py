#!/usr/bin/env python3
"""
Script de teste para validar a triangulação de Delaunay usando a fórmula de Euler
"""

import numpy as np
from delauney import DelaunayTriangulation, gerar_pontos_nao_colineares


def test_delaunay_with_euler(n_points, seed=42):
    """
    Testa a triangulação de Delaunay com n pontos aleatórios não colineares
    e valida usando a fórmula de Euler

    Args:
        n_points: número de pontos a gerar
        seed: semente para reprodutibilidade
    """
    print(f"\n{'='*60}")
    print(f"TESTE COM {n_points} PONTOS ALEATÓRIOS (seed={seed})")
    print(f"{'='*60}\n")

    # Gera pontos não colineares
    print(f"Gerando {n_points} pontos não colineares...")
    points = gerar_pontos_nao_colineares(n_points, min_val=0, max_val=100, seed=seed)
    print(f"✓ Pontos gerados com sucesso!\n")

    # Mostra alguns pontos
    print("Primeiros 5 pontos:")
    for i, p in enumerate(points[:5]):
        print(f"  P{i}: ({p[0]:.2f}, {p[1]:.2f})")
    if n_points > 5:
        print(f"  ... e mais {n_points - 5} pontos\n")

    # Cria e executa a triangulação
    print("Executando triangulação de Delaunay...")
    dt = DelaunayTriangulation()
    dt.add_points(points)
    dt.triangulate()
    print(f"✓ Triangulação concluída!")
    print(f"  Triângulos gerados: {len(dt.triangles)}\n")

    # Valida usando fórmula de Euler
    is_valid, V, E, F, euler_char = dt.validate_euler(verbose=True)

    return is_valid, dt


def main():
    """Executa múltiplos testes com diferentes quantidades de pontos"""

    print("\n" + "="*60)
    print("TESTES DE VALIDAÇÃO DA TRIANGULAÇÃO DE DELAUNAY")
    print("="*60)

    test_cases = [
        (4, 42),    # Caso mínimo
        (10, 123),  # Pequeno
        (25, 456),  # Médio
        (50, 789),  # Grande
        (100, 999), # Muito grande
    ]

    results = []

    for n_points, seed in test_cases:
        try:
            is_valid, dt = test_delaunay_with_euler(n_points, seed)
            results.append((n_points, is_valid))
        except Exception as e:
            print(f"\n✗ ERRO no teste com {n_points} pontos: {e}\n")
            results.append((n_points, False))

    # Resumo final
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    for n_points, is_valid in results:
        status = "✓ PASSOU" if is_valid else "✗ FALHOU"
        print(f"{n_points:3d} pontos: {status}")
    print("="*60)

    # Verifica se todos passaram
    all_passed = all(valid for _, valid in results)
    if all_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM - há bugs no código!")

    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
