import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ProductForm from '../../components/ProductForm'

describe('ProductForm', () => {
  const mockOnSubmit = vi.fn()
  const mockOnCancel = vi.fn()

  it('should render form fields', () => {
    render(<ProductForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)

    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/base buying price/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/base selling price/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/discount percent/i)).toBeInTheDocument()
  })

  it('should call onSubmit with form data when submitted', async () => {
    render(<ProductForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)

    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Test Product' } })
    fireEvent.change(screen.getByLabelText(/base buying price/i), { target: { value: '10' } })
    fireEvent.change(screen.getByLabelText(/base selling price/i), { target: { value: '15' } })

    fireEvent.click(screen.getByRole('button', { name: /create/i }))

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'Test Product',
          baseBuyingPrice: 10,
          baseSellingPrice: 15,
        })
      )
    })
  })

  it('should call onCancel when cancel button is clicked', () => {
    render(<ProductForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)

    fireEvent.click(screen.getByRole('button', { name: /cancel/i }))

    expect(mockOnCancel).toHaveBeenCalled()
  })

  it('should populate form when product prop is provided', () => {
    const product = {
      id: '1',
      name: 'Existing Product',
      baseBuyingPrice: 10,
      baseSellingPrice: 15,
      discountPercent: 10,
    }

    render(<ProductForm product={product} onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)

    expect(screen.getByLabelText(/name/i)).toHaveValue('Existing Product')
    expect(screen.getByLabelText(/base buying price/i)).toHaveValue(10)
    expect(screen.getByLabelText(/base selling price/i)).toHaveValue(15)
    expect(screen.getByRole('button', { name: /update/i })).toBeInTheDocument()
  })
})

