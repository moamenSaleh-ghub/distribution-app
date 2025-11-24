import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import CustomerTable from '../../components/CustomerTable'

describe('CustomerTable', () => {
  const mockOnRowClick = vi.fn()
  const customers = [
    {
      id: '1',
      name: 'Customer 1',
      location: 'Location 1',
      phone: '+1234567890',
      totalDebt: 100.5,
    },
    {
      id: '2',
      name: 'Customer 2',
      location: 'Location 2',
      phone: '+0987654321',
      totalDebt: 0,
    },
  ]

  it('should render customers table', () => {
    render(<CustomerTable customers={customers} onRowClick={mockOnRowClick} loading={false} />)

    expect(screen.getByText('Customer 1')).toBeInTheDocument()
    expect(screen.getByText('Customer 2')).toBeInTheDocument()
  })

  it('should display customer information correctly', () => {
    render(<CustomerTable customers={customers} onRowClick={mockOnRowClick} loading={false} />)

    expect(screen.getByText('Location 1')).toBeInTheDocument()
    expect(screen.getByText('+1234567890')).toBeInTheDocument()
    expect(screen.getByText('$100.50')).toBeInTheDocument()
  })

  it('should call onRowClick when row is clicked', () => {
    render(<CustomerTable customers={customers} onRowClick={mockOnRowClick} loading={false} />)

    const rows = screen.getAllByRole('row')
    fireEvent.click(rows[1]) // First data row (skip header)

    expect(mockOnRowClick).toHaveBeenCalledWith('1')
  })

  it('should show loading message when loading', () => {
    render(<CustomerTable customers={[]} onRowClick={mockOnRowClick} loading={true} />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('should show empty message when no customers', () => {
    render(<CustomerTable customers={[]} onRowClick={mockOnRowClick} loading={false} />)

    expect(screen.getByText(/no customers found/i)).toBeInTheDocument()
  })
})

