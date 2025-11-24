import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import ProductTable from '../../components/ProductTable'

describe('ProductTable', () => {
  const mockOnEdit = vi.fn()
  const products = [
    {
      id: '1',
      name: 'Product 1',
      baseBuyingPrice: 10,
      baseSellingPrice: 15,
      discountPercent: 10,
      effectiveSellingPrice: 13.5,
      isActive: true,
    },
    {
      id: '2',
      name: 'Product 2',
      baseBuyingPrice: 20,
      baseSellingPrice: 25,
      discountPercent: 0,
      effectiveSellingPrice: 25,
      isActive: false,
    },
  ]

  it('should render products table', () => {
    render(<ProductTable products={products} onEdit={mockOnEdit} loading={false} />)

    expect(screen.getByText('Product 1')).toBeInTheDocument()
    expect(screen.getByText('Product 2')).toBeInTheDocument()
  })

  it('should display product prices correctly', () => {
    render(<ProductTable products={products} onEdit={mockOnEdit} loading={false} />)

    expect(screen.getByText('$10.00')).toBeInTheDocument()
    expect(screen.getByText('$15.00')).toBeInTheDocument()
    expect(screen.getByText('$13.50')).toBeInTheDocument()
  })

  it('should show loading message when loading', () => {
    render(<ProductTable products={[]} onEdit={mockOnEdit} loading={true} />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('should show empty message when no products', () => {
    render(<ProductTable products={[]} onEdit={mockOnEdit} loading={false} />)

    expect(screen.getByText(/no products found/i)).toBeInTheDocument()
  })

  it('should call onEdit when edit button is clicked', () => {
    render(<ProductTable products={products} onEdit={mockOnEdit} loading={false} />)

    const editButtons = screen.getAllByRole('button', { name: /edit/i })
    fireEvent.click(editButtons[0])

    expect(mockOnEdit).toHaveBeenCalledWith(products[0])
  })
})

